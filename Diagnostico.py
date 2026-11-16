
import pandas as pd


def diagnosticar_datos(datos):
    print("\n=== DIAGNÓSTICO DE CALIDAD DE DATOS ===")

    print("\n1. Información general:")
    datos.info()
    print("\n2. Valores nulos por columna:")
    print(datos.isnull().sum())

    print("\n3. Filas duplicadas:")
    print(datos.duplicated().sum())

    print("\n4. Fechas duplicadas:")
    print(datos["fecha"].duplicated().sum())

    print("\n5. Fechas inválidas:")
    fechas = pd.to_datetime(datos["fecha"], format="%Y-%m", errors="coerce")
    print(fechas.isnull().sum())

    print("\n6. Valores negativos de generación:")
    print((datos["generacion_bruta_gwh"] < 0).sum())

    print("\n7. Estadísticas de generación:")
    print(datos["generacion_bruta_gwh"].describe())

    return datos
