import streamlit as st
import joblib
import pandas as pd
import numpy as np
import random
import requests

# --- 1. CONFIGURACIÓN  ---
st.set_page_config(page_title="Credit Risk Expert System", layout="wide")

# --- 2. ESTILOS PERSONALIZADOS (CSS) ---
st.markdown("""
    <style>
        h1 {
            text-align: center;
            margin-bottom: 0rem !important;
        }
        .block-container {
            max-width: 1300px;
            padding-top: 1rem;
        }
        [data-testid="stMetricValue"] {
            font-size: 1.4rem;
        }
    </style>
    """, unsafe_allow_html=True)

st.title("Motor de Decisión de Riesgo Crediticio")

# --- 3. ESTRUCTURA DE DISEÑO PRINCIPAL ---
_, centro, _ = st.columns([0.05, 0.9, 0.05])

with centro:
    col1, col2 = st.columns([1.4, 0.8], gap="large")

    # --- COLUMNA IZQUIERDA: ENTRADA DE DATOS ---
    with col1:
        st.header("Parámetros de Evaluación")
        
        with st.container(border=True):
            # Identificación y Validación
            cedula = st.text_input("Número de Identificación", placeholder="Ingrese su Cédula para iniciar...")
            es_valida = False

            if cedula == "":
                st.caption("Esperando identificación...")
            elif not cedula.isdigit():
                st.error("⚠️ Error: Ingrese solo números (sin letras ni puntos).")
            elif len(cedula) != 10:
                st.warning(f"⚠️ La cédula debe tener 10 dígitos (llevas {len(cedula)}).")
            else:
                st.caption(f"Cédula: {int(cedula):,}".replace(",", "."))
                es_valida = True      

            st.markdown("<hr style='margin: -15px 0px 10px 0px;'>", unsafe_allow_html=True)

            # Datos Financieros Básicos
            salario = st.number_input("Salario Mensual (COP)", min_value=0.0, value=5000000.0, format="%.0f")
            st.caption(f"Ref: $ {salario:,.0f}".replace(",", "."))

            # Detalles de la Solicitud
            f_sol_1, f_sol_2 = st.columns(2)
            with f_sol_1:
                monto_solicitado = st.number_input("Monto Solicitado (COP)", min_value=0.0, value=10000000.0, format="%.0f")
                st.caption(f"Ref: $ {monto_solicitado:,.0f}".replace(",", "."))
            with f_sol_2:
                num_cuotas = st.number_input("Plazo (Meses)", min_value=1, max_value=84, value=24)

            st.markdown("<hr style='margin: -15px 0px 10px 0px;'>", unsafe_allow_html=True)
            
            # Gastos y Cálculo de Cuota
            gastos = st.number_input("Gastos Mensuales (COP)", min_value=0.0, value=2000000.0, format="%.0f")
            st.caption(f"Ref: $ {gastos:,.0f}".replace(",", "."))

            tasa_estimada = 0.02 
            cuota_calculada = (monto_solicitado * tasa_estimada) / (1 - (1 + tasa_estimada)**-num_cuotas) if num_cuotas > 0 else 0
            st.info(f"Cuota Mensual Estimada: **$ {cuota_calculada:,.0f}**".replace(",", "."))

    # --- COLUMNA DERECHA: ANÁLISIS Y RESULTADOS ---
    with col2:
        st.header("Análisis")
        
        if not es_valida:
            st.warning("⚠️ Por favor, ingrese el Número de Identificación para habilitar el análisis.")
            st.info("El sistema requiere la identificación para consultar el historial crediticio simulado.")

        elif salario <= 0:
            st.error("Los valores ingresados no son correctos. Por favor, verifique Salario")

        else:
            # 1. Lógica de Capacidad Financiera
            ingreso_disponible = salario - gastos
            ratio_real_disponible = (cuota_calculada / ingreso_disponible) if ingreso_disponible > 0 else 2.0
            ingreso_final_neto = ingreso_disponible - cuota_calculada
            
            # Evaluación de Reglas de Negocio
            errores_logicos = []
            if ratio_real_disponible >= 0.70: 
                errores_logicos.append(f"Endeudamiento Crítico: La cuota consume el {ratio_real_disponible:.0%} de su disponible tras gastos.")
            
            if ingreso_final_neto < 1300000 and salario > 0:
                errores_logicos.append("Riesgo de Subsistencia: El dinero sobrante tras gastos y cuota es inferior al mínimo vital.")

            # 2. Generación de Variables Sintéticas (DataCrédito)
            # Se usa la cédula como semilla para garantizar consistencia
            seed_val = sum(ord(c) for c in cedula)
            random.seed(seed_val)

           # Ajustamos para que el Score rote alrededor de la media de 791 con su desviación de 52
            puntaje_interno = int(np.clip(random.gauss(791, 52), 300, 999))

            # Ajustamos la edad según la media de 42 y std de 11
            edad_simulada = int(np.clip(random.gauss(42, 11), 18, 70))

            # Ajustamos créditos activos (media ~5.8, std ~3.9)
            creditos_activos = int(np.clip(random.gauss(5.8, 3.9), 0, 20))

            # El resto de variables simuladas
            historial_consultas = random.randint(0, 10)
            saldo_total_deudas = creditos_activos * random.randint(500000, 2000000)
            moras_codeudor = 1 if (puntaje_interno < 400 and random.random() > 0.5) else 0
            sector_financiero = 1 if creditos_activos > 0 else 0
            sector_real = int(np.clip(random.gauss(1.3, 1.8), 0, 10))

            # 3. Mapeo de Variables para el Modelo
            all_columns = [
                'huella_consulta', 'tipo_credito_9', 'saldo_principal', 'creditos_sectorReal',
                'plazo_meses', 'puntaje_datacredito', 'cant_creditosvigentes', 'saldo_total',
                'promedio_ingresos_datacredito', 'salario_cliente', 'tipo_credito_68', 'edad_cliente',
                'total_otros_prestamos', 'saldo_mora_codeudor', 'tipo_credito_7', 'tipo_laboral_Independiente',
                'ratio_endeudamiento', 'tipo_credito_10', 'capital_prestado', 'creditos_sectorCooperativo',
                'creditos_sectorFinanciero', 'tipo_credito_6'
            ]
            
            input_data = pd.DataFrame(np.zeros((1, len(all_columns))), columns=all_columns)

            # Limitamos el ratio a un máximo de 2.0 para evitar valores extremos que el modelo no conoce
            ratio_para_modelo = min(ratio_real_disponible, 2.0)

            # Asignación de valores al DataFrame de entrada
            input_data['puntaje_datacredito'] = puntaje_interno
            input_data['edad_cliente'] = edad_simulada
            input_data['cant_creditosvigentes'] = creditos_activos
            input_data['huella_consulta'] = historial_consultas
            input_data['saldo_total'] = saldo_total_deudas
            input_data['saldo_mora_codeudor'] = moras_codeudor
            input_data['creditos_sectorFinanciero'] = sector_financiero
            input_data['creditos_sectorReal'] = sector_real
            input_data['salario_cliente'] = salario
            input_data['capital_prestado'] = monto_solicitado
            input_data['plazo_meses'] = num_cuotas
            input_data['ratio_endeudamiento'] = ratio_para_modelo
            input_data['promedio_ingresos_datacredito'] = ingreso_disponible
            input_data['saldo_principal'] = monto_solicitado

            # 4. Visualización de Perfil Recuperado
            st.subheader("📊 Reporte de Buró de Crédito")
            
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Score", f"{puntaje_interno}")
            m2.metric("Edad", f"{edad_simulada}")
            m3.metric("Créditos", creditos_activos)
            m4.metric("Consultas", historial_consultas)

            with st.expander("Ver detalles de deuda"):
                st.write(f"💰 **Saldo Total:** ${saldo_total_deudas:,.0f}".replace(",", "."))
                st.write(f"💳 **Sector Financiero:** {'Activo' if sector_financiero else 'Sin Reporte'}")
                st.write(f"🏠 **Sector Real:** {sector_real} cuentas abiertas")
            
            st.markdown("---")

            # 5. Lógica de Decisión Final
            if st.button("EVALUAR SOLICITUD"):
                # Primero: Filtro de Score Mínimo
                if puntaje_interno < 350:
                    st.error("❌ TU SOLICITUD HA SIDO RECHAZADA")
                    st.warning(f"Razón: El score recuperado ({puntaje_interno}) es insuficiente para la política de riesgo.")

                # Segundo: Filtro de Capacidad de Pago (Independiente del Score)
                elif errores_logicos:   
                    st.error("❌ RECHAZO: INCUMPLIMIENTO DE POLÍTICA")
                    for err in errores_logicos:
                        st.write(f"• {err}")
                    st.info("Nota: Aunque su historial crediticio sea bueno, su capacidad de pago actual no permite esta obligación.")

                else:
                    try:
                        # Convertimos el DataFrame a un diccionario JSON
                        datos_para_api = input_data.iloc[0].to_dict()
                        
                        # Llamada a la API de FastAPI (Asegúrate de que uvicorn esté corriendo)
                        url_api = "http://127.0.0.1:8000/predict"
                        respuesta = requests.post(url_api, json=datos_para_api)
                        
                        if respuesta.status_code == 200:
                            resultado = respuesta.json()
                            probabilidad = resultado["riesgo"]
                            decision = resultado["decision"]
                            aprobado = resultado["aprobado"]

                            if not aprobado:
                                st.error(f"❌ {decision} POR MODELO ESTADÍSTICO (Riesgo: {probabilidad:.2%})")
                            else:
                                st.success(f"✅ {decision} (Riesgo bajo: {probabilidad:.2%})")
                                if puntaje_interno > 850:
                                    st.caption("Perfil de alta confianza detectado.")
                        else:
                            st.error(f"Error en la API: Código {respuesta.status_code}")
                            
                    except Exception as e:
                      st.error("⚠️ Error de conexión: La API no responde.")
                      st.info("Asegúrate de haber iniciado la API con: uvicorn src.model_deploy:app --reload")


# --- SECCIÓN DE MONITOREO Y DETECCIÓN DE DATA DRIFT ---
# Este panel permite comparar las entradas actuales frente a las medias estadísticas del dataset de entrenamiento.
st.markdown("---")
# Solo mostramos el monitoreo si los datos ya fueron generados/validados
if es_valida:
    with st.expander("🛠️ Panel de Control: Monitoreo de Data Drift"):
        st.write("Análisis de estabilidad de variables: Producción vs. Entrenamiento (Baseline)")
        
        # 1. Parámetros obtenidos del análisis estadístico del dataset original (mean)
        SALARIO_MEAN = 7695748.0
        SCORE_MEAN = 791.46
        EDAD_MEAN = 42.84
        ENDEUDAMIENTO_MEAN = 0.9419 # ratio_endeudamiento (mean)

        col_d1, col_d2, col_d3 = st.columns(3)
        
        # --- Métrica 1: Drift Salarial ---
        # Calculamos la desviación porcentual respecto a la media de 7.69M
        drift_salario = ((salario - SALARIO_MEAN) / SALARIO_MEAN) * 100
        col_d1.metric(
            label="Drift Salarial", 
            value=f"{salario/1e6:.2f}M", 
            delta=f"{drift_salario:.1f}% vs Baseline",
            delta_color="inverse"
        )
        
        # --- Métrica 2: Drift de Score ---
        # La media de puntaje_datacredito en el dataset es de 791.46
        drift_score = ((puntaje_interno - SCORE_MEAN) / SCORE_MEAN) * 100
        col_d2.metric(
            label="Drift de Score", 
            value=f"{puntaje_interno} pts", 
            delta=f"{drift_score:.1f}% vs Baseline",
            delta_color="normal"
        )

        # --- Métrica 3: Drift de Edad ---
        # La media de edad_cliente es de 42.84 años
        drift_edad = ((edad_simulada - EDAD_MEAN) / EDAD_MEAN) * 100
        col_d3.metric(
            label="Drift de Edad", 
            value=f"{edad_simulada} años", 
            delta=f"{drift_edad:.1f}% vs Baseline",
            delta_color="off"
        )

        # 2. Lógica de Alerta de Drift
        # Se activan alertas si el desplazamiento (drift) supera umbrales de tolerancia estadística.
        # Para el salario, dada su alta desviación estándar (std), se establece un umbral del 50%.
        if abs(drift_salario) > 50 or abs(drift_score) > 20:
            st.error("🚨 ALERTA DE DATA DRIFT: Se detectó un desplazamiento significativo en las variables de entrada.")
            st.caption("Nota: El modelo puede presentar degradación en su capacidad predictiva debido a cambios en la población.")
        else:
            st.success("✅ Estabilidad de Datos: Las entradas actuales son coherentes con el perfil de entrenamiento.")

        # 3. Resumen de Calidad del Modelo
        st.info(f"**Análisis de Ratio:** El ratio de endeudamiento actual es de {ratio_real_disponible:.4f} frente a una media histórica de {ENDEUDAMIENTO_MEAN:.4f}.")