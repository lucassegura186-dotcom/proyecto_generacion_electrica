"""Gráficos con Matplotlib Pyplot (Avance 3). Se exportan como PNG."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # sin ventana: permite ejecutar en cualquier equipo
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MaxNLocator

VARIABLE = "generacion_bruta_gwh"
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
         "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
AZUL, NARANJA, GRIS = "#1f4e79", "#d9822b", "#7f7f7f"


def _guardar(fig, ruta):
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(ruta, dpi=160)
    plt.close(fig)
    return ruta


def grafico_01_serie_temporal(datos, ruta):
    """Líneas: evolución mensual con promedio móvil de 12 meses."""
    df = datos.sort_values("fecha")
    movil = df[VARIABLE].rolling(12).mean()
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df["fecha"], df[VARIABLE], color=AZUL, linewidth=1.6, label="Generación mensual")
    ax.plot(df["fecha"], movil, color=NARANJA, linewidth=2.4, label="Promedio móvil 12 meses")
    i_max, i_min = df[VARIABLE].idxmax(), df[VARIABLE].idxmin()
    ax.scatter(df.loc[[i_max], "fecha"], df.loc[[i_max], VARIABLE], color="green", zorder=3, label="Máximo")
    ax.scatter(df.loc[[i_min], "fecha"], df.loc[[i_min], VARIABLE], color="red", zorder=3, label="Mínimo")
    ax.set_title("Evolución de la generación bruta mensual de electricidad en Chile (2018-2026)")
    ax.set_xlabel("Fecha (mes)")
    ax.set_ylabel("Generación bruta (GWh)")
    ax.grid(alpha=0.3)
    ax.legend(loc="upper left")
    return _guardar(fig, ruta)


def grafico_02_histograma(datos, ruta):
    """Histograma: distribución de la generación mensual con media y mediana."""
    valores = datos[VARIABLE].to_numpy(dtype=float)
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.hist(valores, bins=12, color=AZUL, edgecolor="white", alpha=0.9, label="Meses")
    ax.axvline(np.mean(valores), color=NARANJA, linestyle="--", linewidth=2,
               label=f"Media ({np.mean(valores):,.0f} GWh)")
    ax.axvline(np.median(valores), color="green", linestyle=":", linewidth=2,
               label=f"Mediana ({np.median(valores):,.0f} GWh)")
    ax.set_title("Distribución de la generación bruta mensual (105 meses)")
    ax.set_xlabel("Generación bruta mensual (GWh)")
    ax.set_ylabel("Frecuencia (cantidad de meses)")
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.grid(axis="y", alpha=0.3)
    ax.legend()
    return _guardar(fig, ruta)


def grafico_03_barras_comparables(datos, ruta):
    """Barras: generación acumulada de los mismos meses (ene-último mes) en cada año."""
    ultimo_mes = int(datos.loc[datos["anio"] == datos["anio"].max(), "mes"].max())
    comparable = datos[datos["mes"] <= ultimo_mes].groupby("anio")[VARIABLE].sum().sort_index()
    colores = [NARANJA if a == comparable.index.max() else AZUL for a in comparable.index]
    fig, ax = plt.subplots(figsize=(9, 5))
    barras = ax.bar(comparable.index.astype(str), comparable.values, color=colores)
    ax.bar_label(barras, labels=[f"{v:,.0f}" for v in comparable.values], padding=3, fontsize=8)
    ax.set_title(f"Generación bruta acumulada de enero a {MESES[ultimo_mes - 1]} por año")
    ax.set_xlabel("Año")
    ax.set_ylabel("Generación acumulada (GWh)")
    ax.set_ylim(0, comparable.max() * 1.25)
    ax.grid(axis="y", alpha=0.3)
    ax.legend(handles=[plt.Rectangle((0, 0), 1, 1, color=AZUL), plt.Rectangle((0, 0), 1, 1, color=NARANJA)],
              labels=["Años anteriores", "Último año disponible"], loc="upper left")
    return _guardar(fig, ruta)


def generar_graficos(datos, carpeta):
    carpeta = Path(carpeta)
    return [
        grafico_01_serie_temporal(datos, carpeta / "grafico_01.png"),
        grafico_02_histograma(datos, carpeta / "grafico_02.png"),
        grafico_03_barras_comparables(datos, carpeta / "grafico_03.png"),
    ]
