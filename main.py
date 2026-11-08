"""Punto de entrada: ejecuta todo el proceso con `python main.py` desde la raíz."""

from pathlib import Path

import pandas as pd

from src.carga import cargar_datos
from src.Diagnostico import diagnosticar_datos
from src.limpieza import limpiar_datos
from src.transformaciones import transformar_datos
from src.validaciones import validar_datos
from src.estadisticas import calcular_estadisticas, exportar_estadisticas
from src.indicadores import calcular_indicadores, exportar_indicadores
from src.visualizaciones import generar_graficos

RAIZ = Path(__file__).resolve().parent
RUTA_ORIGINAL = RAIZ / "Datos" / "Originales" / "Dataset_original.csv"
RUTA_LIMPIO = RAIZ / "Datos" / "procesados" / "dataset_limpio.csv"
CARPETA_RESULTADOS = RAIZ / "resultados"


def main():
    # --- Avance 2: preparación de datos ---
    datos = cargar_datos(RUTA_ORIGINAL)
    diagnosticar_datos(datos)
    datos = transformar_datos(limpiar_datos(datos))
    validar_datos(datos)
    RUTA_LIMPIO.parent.mkdir(parents=True, exist_ok=True)
    datos.to_csv(RUTA_LIMPIO, index=False, date_format="%Y-%m-%d")
    print(f"\nArchivo limpio exportado correctamente: {RUTA_LIMPIO.relative_to(RAIZ)}")

    # --- Avance 3: el análisis parte del dataset limpio exportado ---
    print("\n=== AVANCE 3: ANÁLISIS ===")
    limpio = pd.read_csv(RUTA_LIMPIO, parse_dates=["fecha"])
    print(f"Dataset limpio leído: {len(limpio)} registros")

    estadisticas = calcular_estadisticas(limpio)
    exportar_estadisticas(estadisticas, CARPETA_RESULTADOS / "estadisticas.csv")
    print("\nEstadísticas descriptivas:")
    print(estadisticas.to_string(index=False))

    indicadores = calcular_indicadores(limpio)
    exportar_indicadores(indicadores, CARPETA_RESULTADOS / "indicadores.csv")
    print("\nIndicadores:")
    print(indicadores[["indicador", "resultado", "unidad"]].to_string(index=False))

    graficos = generar_graficos(limpio, CARPETA_RESULTADOS / "graficos")
    print("\nGráficos generados:")
    for g in graficos:
        print(" -", g.relative_to(RAIZ))

    print("\nProceso completado. Resultados en la carpeta 'resultados/'.")


if __name__ == "__main__":
    main()
