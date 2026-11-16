"""Estadística descriptiva de la generación bruta mensual (Avance 3)."""

from pathlib import Path

import numpy as np
import pandas as pd

NOMBRES_MESES = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio",
    7: "Julio", 8: "Agosto", 9: "Septiembre", 10: "Octubre",
    11: "Noviembre", 12: "Diciembre",
}

VARIABLE = "generacion_bruta_gwh"


def calcular_estadisticas(datos):
    """Devuelve una tabla con medidas descriptivas y frecuencias categóricas."""
    valores = datos[VARIABLE].to_numpy(dtype=float)
    q1, q2, q3 = np.percentile(valores, [25, 50, 75])

    medidas = [
        ("Cantidad de registros", len(valores), "meses"),
        ("Media", np.mean(valores), "GWh"),
        ("Mediana", np.median(valores), "GWh"),
        ("Mínimo", np.min(valores), "GWh"),
        ("Máximo", np.max(valores), "GWh"),
        ("Rango", np.ptp(valores), "GWh"),
        ("Desviación estándar", np.std(valores, ddof=1), "GWh"),
        ("Primer cuartil (Q1)", q1, "GWh"),
        ("Segundo cuartil (Q2)", q2, "GWh"),
        ("Tercer cuartil (Q3)", q3, "GWh"),
        ("Rango intercuartílico (Q3-Q1)", q3 - q1, "GWh"),
    ]
    filas = [("numerica", VARIABLE, m, v, u) for m, v, u in medidas]

    # Frecuencias de las variables categóricas (año y mes calendario).
    for categoria, frecuencia in datos["anio"].value_counts().sort_index().items():
        filas.append(("categorica", "anio", f"Frecuencia {categoria}", int(frecuencia), "meses"))

    frec_mes = datos["mes"].value_counts().sort_index()
    for mes, frecuencia in frec_mes.items():
        filas.append(("categorica", "mes", f"Frecuencia {NOMBRES_MESES[int(mes)]}", int(frecuencia), "años"))

    return pd.DataFrame(filas, columns=["tipo", "variable", "medida", "valor", "unidad"])


def exportar_estadisticas(estadisticas, ruta):
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    estadisticas.to_csv(ruta, index=False, encoding="utf-8-sig")
    return ruta
