from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np

# Inicializar la App
app = FastAPI(
    title="API de Riesgo Crediticio",
    description="Servicio de inferencia para el sistema experto de crédito",
    version="1.0.0"
)

# Cargar el modelo (buscamos un nivel arriba ya que el modelo suele estar en la raíz)
model = joblib.load('modelo_riesgo_final.joblib')

# Definir el esquema de datos de entrada (las variables que usa tu modelo)
class SolicitudCredito(BaseModel):
    huella_consulta: int
    tipo_credito_9: int
    saldo_principal: float
    creditos_sectorReal: int
    plazo_meses: int
    puntaje_datacredito: int
    cant_creditosvigentes: int
    saldo_total: float
    promedio_ingresos_datacredito: float
    salario_cliente: float
    tipo_credito_68: int
    edad_cliente: int
    total_otros_prestamos: float
    saldo_mora_codeudor: int
    tipo_credito_7: int
    tipo_laboral_Independiente: int
    ratio_endeudamiento: float
    tipo_credito_10: int
    capital_prestado: float
    creditos_sectorCooperativo: int
    creditos_sectorFinanciero: int
    tipo_credito_6: int

@app.get("/")
def home():
    return {"mensaje": "API de Riesgo Crediticio Activa. Use el endpoint /predict"}

@app.post("/predict")
def predict(data: SolicitudCredito):
    # 1. Convertir el objeto Pydantic a diccionario y luego a DataFrame
    input_df = pd.DataFrame([data.model_dump()])
    
    # 2. Asegurar el orden correcto de las columnas para el modelo
    all_columns = [
        'huella_consulta', 'tipo_credito_9', 'saldo_principal', 'creditos_sectorReal',
        'plazo_meses', 'puntaje_datacredito', 'cant_creditosvigentes', 'saldo_total',
        'promedio_ingresos_datacredito', 'salario_cliente', 'tipo_credito_68', 'edad_cliente',
        'total_otros_prestamos', 'saldo_mora_codeudor', 'tipo_credito_7', 'tipo_laboral_Independiente',
        'ratio_endeudamiento', 'tipo_credito_10', 'capital_prestado', 'creditos_sectorCooperativo',
        'creditos_sectorFinanciero', 'tipo_credito_6'
    ]
    input_df = input_df[all_columns]
    
    # 3. Realizar la predicción
    probabilidad = model.predict_proba(input_df)[0][1]
    clase = int(probabilidad > 0.40) # Mismo umbral que usamos en Streamlit
    
    return {
        "riesgo": round(probabilidad, 4),
        "aprobado": bool(clase == 0),
        "decision": "RECHAZADO" if clase == 1 else "APROBADO"
    }