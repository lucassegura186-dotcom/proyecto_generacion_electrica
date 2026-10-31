from pathlib import Path

from src.carga import cargar_datos
from src.Diagnostico import diagnosticar_datos
from src.limpieza import limpiar_datos
from src.transformaciones import transformar_datos
from src.validaciones import validar_datos


def main():
    ruta = "Datos/originales/dataset_original.csv"

    datos = cargar_datos(ruta)
    diagnosticar_datos(datos)

    datos_limpios = limpiar_datos(datos)
    datos_transformados = transformar_datos(datos_limpios)

    validar_datos(datos_transformados)

    ruta_salida = Path("Datos/procesados/dataset_limpio.csv")
    ruta_salida.parent.mkdir(parents=True, exist_ok=True)

    datos_transformados.to_csv(
        ruta_salida,
        index=False,
        date_format="%Y-%m-%d"
    )

    print("\nArchivo limpio exportado correctamente.")
    print(f"Ubicación: {ruta_salida}")


if __name__ == "__main__":
    main()