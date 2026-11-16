from pathlib import Path
import pandas as pd


def cargar_datos(ruta):
    ruta = Path(ruta)

    if not ruta.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {ruta}")

    datos = pd.read_csv(ruta)

    if datos.empty:
        raise ValueError("El archivo CSV no contiene registros.")

    print("=== CARGA DE DATOS ===")
    print("Archivo cargado correctamente.")
    print(f"Filas: {datos.shape[0]}")
    print(f"Columnas: {datos.shape[1]}")

    print("\nPrimeros registros:")
    print(datos.head())

    print("\nTipos de datos:")
    print(datos.dtypes)

    return datos