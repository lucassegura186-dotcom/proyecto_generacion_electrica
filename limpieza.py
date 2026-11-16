
import pandas as pd


def limpiar_datos(datos):
    print("\n=== LIMPIEZA DE DATOS ===")

    datos = datos.copy()

    # Normalizar nombres de columnas
    datos.columns = datos.columns.str.strip().str.lower()

    # Convertir la fecha a formato datetime
    datos["fecha"] = pd.to_datetime(
        datos["fecha"],
        format="%Y-%m",
        errors="coerce"
    )

    # Convertir la generación a formato numérico
    datos["generacion_bruta_gwh"] = pd.to_numeric(
        datos["generacion_bruta_gwh"],
        errors="coerce"
    )

    # Eliminar registros con datos inválidos
    filas_antes = len(datos)
    datos = datos.dropna(
        subset=["fecha", "generacion_bruta_gwh"]
    )
    filas_eliminadas = filas_antes - len(datos)

    # Eliminar filas duplicadas
    duplicados = datos.duplicated().sum()
    datos = datos.drop_duplicates()

    print(f"Registros eliminados por datos inválidos: {filas_eliminadas}")
    print(f"Registros duplicados eliminados: {duplicados}")
    print(f"Filas finales: {len(datos)}")

    return datos
