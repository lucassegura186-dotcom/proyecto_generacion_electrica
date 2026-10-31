
def transformar_datos(datos):
    print("\n=== TRANSFORMACIÓN DE DATOS ===")

    datos = datos.copy()

    # Extraer el año de la fecha
    datos["anio"] = datos["fecha"].dt.year

    # Extraer el mes de la fecha
    datos["mes"] = datos["fecha"].dt.month

    print("Columnas temporales agregadas correctamente.")
    print("\nPrimeros registros transformados:")
    print(datos.head())

    print("\nColumnas finales:")
    print(datos.columns.tolist())

    return datos
