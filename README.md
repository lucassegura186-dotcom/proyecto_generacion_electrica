# Análisis estadístico de la generación eléctrica mensual en Chile

Proyecto Final Integrador de Programación Avanzada – Grupo 13
(Laura Meza, Cesar Antiqueo, Lucas Segura). Docente: Alex Flores Fuentealba.

## Descripción del proyecto

Análisis de la generación bruta mensual de energía eléctrica en Chile entre enero de 2018 y
septiembre de 2026 (105 registros, en GWh), usando Python, Pandas, NumPy y Matplotlib.

Pregunta del proyecto: ¿cómo cambia la generación eléctrica entre los meses y qué variaciones
se observan durante el período estudiado?

## Avances

| Avance | Contenido | Informe |
|--------|-----------|---------|
| 1 | Planteamiento del problema, carga de datos | `reportes/avance_1.pdf` |
| 2 | Diagnóstico, limpieza, transformación y validación | `reportes/avance_2.pdf` |
| 3 | Estadísticas descriptivas, indicadores y gráficos | `reportes/avance_3.pdf` |

## Estructura del proyecto

```
proyecto_generacion_electrica/
├── Datos/
│   ├── Originales/Dataset_original.csv     # datos originales (sin modificar)
│   └── procesados/dataset_limpio.csv       # dataset limpio (Avance 2)
├── resultados/
│   ├── estadisticas.csv                    # estadísticas descriptivas y frecuencias
│   ├── indicadores.csv                     # indicadores automatizados
│   └── graficos/                           # grafico_01.png, grafico_02.png, grafico_03.png
├── reportes/                               # avance_1.pdf, avance_2.pdf, avance_3.pdf
├── src/
│   ├── carga.py            # carga el CSV
│   ├── Diagnostico.py      # diagnóstico de calidad
│   ├── limpieza.py         # limpieza
│   ├── transformaciones.py # agrega año y mes
│   ├── validaciones.py     # valida el dataset transformado
│   ├── estadisticas.py     # Avance 3: estadística descriptiva
│   ├── indicadores.py      # Avance 3: indicadores automatizados
│   └── visualizaciones.py  # Avance 3: gráficos con Pyplot
├── main.py                 # ejecuta todo el proceso
├── requirements.txt
└── README.md
```

## Instalación y ejecución

Desde la carpeta principal del proyecto:

```bash
python -m pip install -r requirements.txt
python main.py
```

Al ejecutar `main.py` se limpia el dataset, se calculan las estadísticas y los indicadores y se
generan los gráficos automáticamente.

## Resultados del Avance 3

- `resultados/estadisticas.csv`: cantidad de registros, media, mediana, mínimo, máximo, rango,
  desviación estándar, cuartiles, rango intercuartílico y frecuencias de año y mes.
- `resultados/indicadores.csv`: ocho indicadores con método de cálculo, resultado, unidad e
  interpretación (registros válidos, promedio mensual, máximo y mínimo con su fecha, variación
  anual comparable, % de meses sobre el promedio, meses críticos y coeficiente de variación).
- `resultados/graficos/grafico_01.png`: evolución mensual (líneas, con promedio móvil de 12 meses).
- `resultados/graficos/grafico_02.png`: distribución de la generación mensual (histograma).
- `resultados/graficos/grafico_03.png`: generación acumulada enero-septiembre por año (barras).

**Nota:** 2026 solo tiene datos hasta septiembre, por lo que la variación anual y el gráfico de
barras comparan siempre los mismos meses (enero-septiembre) de cada año.

## Fuente de datos

Comisión Nacional de Energía (CNE), plataforma Energía Abierta:
https://energiaabierta.cl/categorias-estadistica/electricidad/
