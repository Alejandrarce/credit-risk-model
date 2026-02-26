Credit Risk Model

Este repositorio contiene el desarrollo de un modelo de Machine Learning diseñado para predecir el riesgo crediticio. El objetivo principal es clasificar a los solicitantes de crédito en categorías de riesgo para optimizar la toma de decisiones financieras.

- Caso de Negocio y Objetivos.

    El riesgo de impago es uno de los mayores desafíos en el sector financiero. Este proyecto busca automatizar la detección de clientes con alta probabilidad de incumplimiento utilizando datos históricos.

        Objetivo Técnico: Desarrollar un modelo de clasificación binaria.

        Métrica de Negocio: Se priorizó el Recall (0.57) sobre la Precisión, ya que para la entidad financiera es más costoso no detectar a un cliente moroso que investigar a un cliente cumplido por error (Falsos Positivos).

- Hallazgos Principales (EDA).

    Tras el análisis exploratorio de datos, se identificaron los siguientes puntos críticos:

        Desbalanceo de Clases: La mayoría de los clientes pertenecen a la categoría de bajo riesgo, lo que requirió un ajuste en los umbrales de decisión del modelo.

        Correlaciones Clave: El historial crediticio previo y el monto del préstamo en relación con los ingresos anuales son los predictores más fuertes del riesgo.

        Calidad de Datos: Se realizó un tratamiento de valores nulos y una codificación de variables categóricas para asegurar la compatibilidad con el algoritmo de Regresión Logística.

- Arquitectura y Versionamiento

    El proyecto sigue una arquitectura de carpetas estrictamente definida para garantizar la escalabilidad y el uso de pipelines de CI/CD:

        src/: Contiene los notebooks de EDA (comprension_eda.ipynb) y los scripts de ingeniería de características y evaluación.

        main: Rama de producción con versiones estables y certificadas.

        developer: Rama de desarrollo para integración de nuevas características.

        certification: Rama espejo para pruebas de calidad.

        Nota de Auditoría: El historial de versiones incluye etiquetas (v1.0.1, v1.1.0) y registros de aprobación de pares evaluadores para asegurar la trazabilidad del proceso.