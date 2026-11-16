"""Proyecciones mensuales simples; no constituyen predicciones causales."""
import numpy as np
import pandas as pd


def proyectar(serie, horizonte=12, ventana=12, modelo='Ambos'):
    s = serie.dropna().sort_index().astype(float)
    if len(s) < 3:
        raise ValueError('Se requieren al menos tres meses históricos.')
    if not isinstance(s.index, pd.DatetimeIndex):
        raise ValueError('La serie debe estar indexada por fecha.')
    if horizonte < 1 or ventana < 2 or ventana > len(s):
        raise ValueError('Revisa el horizonte y la ventana seleccionados.')
    fechas = pd.date_range(s.index.max() + pd.offsets.MonthBegin(1), periods=horizonte, freq='MS')
    t = np.arange(len(s), dtype=float)
    futuro = np.arange(len(s), len(s) + horizonte, dtype=float)
    pendiente, intercepto = np.polyfit(t, s.to_numpy(), 1)
    regresion = np.maximum(0, pendiente * futuro + intercepto)
    # Pronóstico constante basado en los últimos N meses; no es un promedio móvil recursivo.
    promedio = np.full(horizonte, float(s.tail(ventana).mean()))
    salida = pd.DataFrame(index=fechas)
    if modelo in ('Ambos', 'Regresión lineal'):
        salida['Regresión lineal'] = regresion
    if modelo in ('Ambos', 'Promedio móvil'):
        salida['Promedio móvil'] = promedio
    salida.index.name = 'fecha'
    return salida


def evaluar_modelos(serie, ventana=12, prueba=12):
    """Evaluación temporal: últimos meses reservados como test, sin entrenar con ellos."""
    s = serie.dropna().sort_index().astype(float)
    if len(s) < max(ventana + 3, prueba + 6):
        return None
    train, test = s.iloc[:-prueba], s.iloc[-prueba:]
    if len(train) < ventana:
        return None
    pred = proyectar(train, len(test), ventana, 'Ambos')
    result = {}
    for col in pred.columns:
        error = np.abs(test.to_numpy() - pred[col].to_numpy())
        result[col] = float(error.mean())
    return result
