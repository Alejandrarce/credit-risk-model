import pandas as pd
import os
import sys

def importar_dataset(ruta):
    """
    Carga el archivo CSV y realiza una validación inicial.
    """
    print(f"--- Iniciando carga de datos desde: {ruta} ---")
    
    if not os.path.exists(ruta):
        print(f"ERROR: No se encuentra el archivo en {ruta}")
        sys.exit(1) # Finaliza el script con error para que Jenkins lo detecte
        
    try:
        df = pd.read_csv(ruta)
        print(f"ÉXITO: Archivo cargado correctamente.")
        print(f"Filas: {df.shape[0]} | Columnas: {df.shape[1]}")
        
        # Validación rápida de calidad
        nulos = df.isnull().sum().sum()
        if nulos > 0:
            print(f"AVISO: Se detectaron {nulos} valores nulos en el dataset.")
        
        return df
    except Exception as e:
        print(f"ERROR inesperado al leer el CSV: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Definimos la ruta relativa desde la carpeta 'src' hacia la raíz
    RUTA_DATOS = os.path.join('..', 'Base_de_datos.csv')
    
    # Ejecutamos la función
    df = importar_dataset(RUTA_DATOS)
    
    # Guardamos una pequeña muestra o log si es necesario
    print("--- Proceso de carga finalizado ---")