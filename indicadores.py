"""Indicadores automatizados de la generación bruta mensual (Avance 3)."""

from pathlib import Path

import numpy as np
import pandas as pd

VARIABLE = "generacion_bruta_gwh"
ABREV_MESES = {1: "ene", 2: "feb", 3: "mar", 4: "abr", 5: "may", 6: "jun",
               7: "jul", 8: "ago", 9: "sep", 10: "oct", 11: "nov", 12: "dic"}


def _fmt(numero, decimales=1):
    """Formato con separador de miles y coma decimal (estilo chileno)."""
    texto = f"{numero:,.{decimales}f}"
    return texto.replace(",", "X").replace(".", ",").replace("X", ".")


def calcular_indicadores(datos):
    """Devuelve la tabla: indicador, método de cálculo, resultado, unidad, interpretación."""
    df = datos.sort_values("fecha").reset_index(drop=True)
    valores = df[VARIABLE].to_numpy(dtype=float)
    media = np.mean(valores)
    desv = np.std(valores, ddof=1)

    i_max, i_min = int(np.argmax(valores)), int(np.argmin(valores))
    fecha_max, fecha_min = df.loc[i_max, "fecha"], df.loc[i_min, "fecha"]

    # Variación entre períodos comparables: mismos meses del último año y del anterior.
    ultimo_anio = int(df["anio"].max())
    ultimo_mes = int(df.loc[df["anio"] == ultimo_anio, "mes"].max())
    periodo = df["mes"] <= ultimo_mes
    actual = df.loc[periodo & (df["anio"] == ultimo_anio), VARIABLE].sum()
    anterior = df.loc[periodo & (df["anio"] == ultimo_anio - 1), VARIABLE].sum()
    variacion = (actual / anterior - 1) * 100 if anterior else np.nan

    sobre_media = np.mean(valores > media) * 100
    criticos = int(np.sum(np.abs(valores - media) > desv))
    cv = desv / media * 100

    filas = [
        ("Total de registros válidos",
         "Conteo de filas del dataset limpio sin nulos, duplicados ni negativos.",
         len(valores), "meses",
         f"Se analizan {len(valores)} meses ({df['fecha'].min():%Y-%m} a {df['fecha'].max():%Y-%m}); "
         "la serie es completa y confiable."),
        ("Generación promedio mensual",
         "Media aritmética de generacion_bruta_gwh.",
         media, "GWh/mes",
         f"Un mes típico genera cerca de {_fmt(media)} GWh."),
        ("Mes de mayor generación",
         "Valor máximo de la serie y su fecha asociada.",
         valores[i_max], "GWh",
         f"El máximo ocurrió en {fecha_max:%Y-%m}; supera a la media en "
         f"{_fmt((valores[i_max] / media - 1) * 100)} %."),
        ("Mes de menor generación",
         "Valor mínimo de la serie y su fecha asociada.",
         valores[i_min], "GWh",
         f"El mínimo ocurrió en {fecha_min:%Y-%m}; queda "
         f"{_fmt((1 - valores[i_min] / media) * 100)} % bajo la media."),
        (f"Variación anual comparable (ene-{ABREV_MESES[ultimo_mes]} de {ultimo_anio} vs {ultimo_anio - 1})",
         "(Suma ene-último mes del último año / suma de los mismos meses del año anterior - 1) x 100.",
         variacion, "%",
         f"Con los mismos meses, la generación {'aumentó' if variacion >= 0 else 'disminuyó'} "
         f"{_fmt(abs(variacion), 2)} % respecto del año anterior."),
        ("Porcentaje de meses sobre el promedio",
         "(Meses con generación > media / total de meses) x 100.",
         sobre_media, "%",
         f"{_fmt(sobre_media)} % de los meses supera la media; el resto queda por debajo, "
         "lo que indica una distribución bastante equilibrada en torno a ella."),
        ("Cantidad de meses críticos (atípicos)",
         "Conteo de meses con |generación - media| > 1 desviación estándar.",
         criticos, "meses",
         f"{criticos} meses se alejan más de {_fmt(desv)} GWh de la media; son los meses atípicos de la serie."),
        ("Coeficiente de variación mensual",
         "(Desviación estándar / media) x 100.",
         cv, "%",
         f"La variabilidad relativa es {'baja' if cv < 10 else 'moderada'}: la generación mensual es bastante estable."),
    ]
    return pd.DataFrame(filas, columns=["indicador", "metodo_calculo", "resultado", "unidad", "interpretacion"])


def exportar_indicadores(indicadores, ruta):
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    indicadores.to_csv(ruta, index=False, encoding="utf-8-sig")
    return ruta
