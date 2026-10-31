import pandas as pd

def validar_datos(datos):
    print("\n=== VALIDACIÓN DE DATOS TRANSFORMADOS ===")

    columnas_esperadas = [
        "fecha",
        "generacion_bruta_gwh",
        "anio",
        "mes"
    ]

    faltantes = [
        columna for columna in columnas_esperadas
        if columna not in datos.columns
    ]

    print("\n1. Columnas faltantes:")
    print(faltantes)

    if faltantes:
        raise ValueError(f"Faltan columnas: {faltantes}")

    print("\n2. Valores nulos:")
    print(datos.isnull().sum())

    print("\n3. Filas duplicadas:")
    print(datos.duplicated().sum())

    print("\n4. Tipo de dato de fecha:")
    print(datos["fecha"].dtype)

    print("\n5. Valores negativos:")
    print((datos["generacion_bruta_gwh"] < 0).sum())

    print("\n6. Cantidad de registros:")
    print(len(datos))

    if datos.isnull().any().any():
        raise ValueError("Existen valores nulos.")

    if datos.duplicated().any():
        raise ValueError("Existen filas duplicadas.")

    if not pd.api.types.is_datetime64_any_dtype(datos["fecha"]):
        raise ValueError("La columna fecha no tiene formato datetime.")

    if (datos["generacion_bruta_gwh"] < 0).any():
        raise ValueError("Existen valores negativos.")

    if not datos["mes"].between(1, 12).all():
        raise ValueError("Existen meses fuera del rango válido.")

    print("\nValidación completada correctamente.")

    return datos