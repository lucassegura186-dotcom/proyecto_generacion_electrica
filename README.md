# Análisis estadístico de la generación eléctrica mensual en Chile

## Descripción del proyecto

Este proyecto busca analizar la generación bruta mensual de energía eléctrica en Chile, considerando los datos disponibles desde enero de 2018 hasta septiembre de 2026.

Para preparar la información se utiliza Python y la biblioteca Pandas. Durante este avance se trabajó en la carga, diagnóstico, limpieza, transformación y validación del conjunto de datos.

## Objetivo

Preparar un conjunto de datos limpio y organizado que permita realizar posteriormente un análisis estadístico de la generación eléctrica mensual en Chile.

## Estructura del proyecto

- `Datos/`: contiene los archivos originales y procesados.
  - `Originales/`: contiene el archivo CSV original.
  - `procesados/`: contiene el conjunto de datos limpio.
- `src/`: contiene los módulos de Python.
  - `carga.py`: carga el archivo CSV.
  - `Diagnostico.py`: realiza el diagnóstico de calidad de los datos.
  - `limpieza.py`: limpia y organiza los registros.
  - `transformaciones.py`: agrega las columnas de año y mes.
  - `validaciones.py`: comprueba la calidad de los datos transformados.
  - `main.py`: organiza y ejecuta el proceso completo.
- `reportes/`: contiene los informes y evidencias del proyecto.
- `main.py`: permite ejecutar el proceso desde la carpeta principal.
- `requirements.txt`: contiene las dependencias del proyecto.
- `README.md`: contiene la documentación del proyecto.

## Requisitos

- Python 3.
- Pandas 3.1.0.

## Instalación

Desde la carpeta principal del proyecto, instalar las dependencias con:

```bash
python -m pip install -r requirements.txt
```

## Ejecución

Desde la carpeta principal del proyecto, ejecutar:

```bash
python main.py
```

## Resultado

El proceso genera el archivo `dataset_limpio.csv`, ubicado en:

`Datos/procesados/dataset_limpio.csv`

El archivo contiene las siguientes columnas:

- `fecha`
- `generacion_bruta_gwh`
- `anio`
- `mes`

## Fuente de datos

Comisión Nacional de Energía (CNE), plataforma Energía Abierta:

https://energiaabierta.cl/categorias-estadistica/electricidad/
