Motor de Decisión de Riesgo Crediticio (Credit Risk Expert System) 

Este ecosistema integra modelos de Machine Learning y motores de reglas de negocio para la evaluación automatizada de solicitudes financieras. El sistema no solo predice la probabilidad de incumplimiento, sino que garantiza la salud financiera de la entidad mediante monitoreo estadístico y filtros de capacidad de pago.

- Caso de Negocio y Objetivos Operativos

    El riesgo de impago representa el principal desafío en el sector financiero. Este sistema optimiza la colocación de activos mediante un enfoque dual:

    Filtros de Política y Liquidez: Antes del análisis predictivo, el sistema evalúa parámetros de banca responsable. Se implementan filtros de "Mínimo Vital" y "Capacidad de Pago". Un hallazgo crítico en la fase de validación demostró que perfiles con Score crediticio superior a 790 pueden ser declinados si el ratio de endeudamiento compromete la subsistencia del cliente, priorizando la liquidez real sobre el historial estático.

    Métrica de Rendimiento: Se prioriza el Recall (0.57) sobre la precisión absoluta, minimizando el riesgo de falsos negativos (clientes morosos no detectados), lo cual optimiza el costo operativo de la cartera.

- Implementación Tecnológica

    1. Sistema Experto (Streamlit Interface)
    Se desarrolló una interfaz de alta fidelidad para la captura de datos y visualización de resultados. El sistema realiza una simulación de variables de buró de crédito mediante Distribuciones Gaussianas basadas en las estadísticas descriptivas del dataset de entrenamiento, permitiendo pruebas de estrés con coherencia estadística respecto a la población objetivo.

    2. Detección de Data Drift (Monitoreo de Deriva)
    Para garantizar la vigencia del modelo en producción, se implementó un panel de control que monitorea el desplazamiento de las variables de entrada frente al baseline estadístico:

    Baseline Salarial: Media de 7.69M COP.

    Baseline de Score: Media de 791.46 pts.
    El sistema genera alertas automáticas ante desviaciones significativas (Drift), indicando cambios en el comportamiento del mercado o de la población solicitante que requieran un reentrenamiento del modelo.

    3. Ingeniería de Robustez y CI/CD
    Clipping de Variables: Se aplica una técnica de recorte al ratio de endeudamiento (máximo 2.0) para prevenir la inestabilidad en las inferencias del modelo ante valores atípicos (outliers).

    Integración Continua (CI/CD): Se utiliza GitHub Actions para automatizar la validación de sintaxis, pruebas de dependencias y estabilidad del entorno en cada despliegue, asegurando la continuidad operativa.

- Arquitectura de Datos y Trazabilidad

    src/: Notebooks de análisis exploratorio (EDA), ingeniería de características y evaluación del modelo.

    app.py: Núcleo del motor de decisión y panel de monitoreo técnico.

    .github/workflows/: Pipelines de automatización para CI/CD.

    El versionamiento del sistema sigue estándares de auditoría técnica con etiquetas de versión (v1.x.x) y segregación de ramas por estado de certificación (main, developer, certification), garantizando la trazabilidad absoluta de cada mejora en el algoritmo.