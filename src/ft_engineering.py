import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

def ft_engineering(df):
    """
    Componente de ingeniería de características.
    Retorna X_train, X_test, y_train, y_test y el preprocesador.
    """
    # 1. Definir Target y Variables (X)
    # Eliminamos Pago_atiempo de X y la dejamos en y
    X = df.drop(columns=['Pago_atiempo'])
    y = df['Pago_atiempo']
    
    # 2. Identificar tipos de columnas para el ColumnTransformer
    # Tomamos las numéricas (salario, edad, puntaje, etc.)
    numeric_features = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
    # Tomamos las categóricas (las que no se volvieron dummies aún o nuevas)
    categorical_features = X.select_dtypes(include=['object', 'category']).columns.tolist()

    # 3. Construcción del Pipeline según el diagrama entregado
    # Pipeline Numérico: Imputación -> Escalado
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    # Pipeline Categórico: Imputación -> OneHot
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore', drop='first'))
    ])

    # 4. ColumnTransformer: El integrador
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ]
    )

    # 5. Split de Datos con Estratificación (Manejo de desbalanceo)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    print(f"Ingeniería terminada. Train: {X_train.shape[0]} | Test: {X_test.shape[0]}")
    return X_train, X_test, y_train, y_test, preprocessor