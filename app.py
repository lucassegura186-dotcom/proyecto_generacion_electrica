"""Dashboard Avance 4. Ejecutar: streamlit run app.py"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from src.proyecciones import proyectar, evaluar_modelos

RAIZ = Path(__file__).resolve().parent
CSV = RAIZ / 'Datos' / 'procesados' / 'dataset_limpio.csv'

st.set_page_config(page_title='Generación eléctrica de Chile', page_icon='⚡', layout='wide')
st.title('⚡ Generación eléctrica de Chile')
st.caption('Avance 4 · Exploración histórica y escenarios de proyección · Unidad: GWh mensuales')

@st.cache_data
def cargar_csv(ruta, mtime):
    df = pd.read_csv(ruta, parse_dates=['fecha'])
    if not {'fecha', 'generacion_bruta_gwh'}.issubset(df.columns):
        raise ValueError('El CSV debe incluir fecha y generacion_bruta_gwh.')
    df = df[['fecha', 'generacion_bruta_gwh']].copy()
    df['generacion_bruta_gwh'] = pd.to_numeric(df['generacion_bruta_gwh'], errors='coerce')
    df = df.dropna().sort_values('fecha').drop_duplicates('fecha')
    df['fecha'] = df['fecha'].dt.to_period('M').dt.to_timestamp()
    df = df.groupby('fecha', as_index=False)['generacion_bruta_gwh'].sum()
    df['anio'] = df.fecha.dt.year
    df['mes'] = df.fecha.dt.month
    return df

if not CSV.exists():
    st.error(f'No se encuentra el dataset: {CSV}')
    st.stop()
try:
    df = cargar_csv(str(CSV), CSV.stat().st_mtime)
except Exception as exc:
    st.error(f'Error al leer el dataset: {exc}')
    st.stop()

anios = sorted(df.anio.unique().tolist())
meses = {1:'Enero',2:'Febrero',3:'Marzo',4:'Abril',5:'Mayo',6:'Junio',7:'Julio',8:'Agosto',9:'Septiembre',10:'Octubre',11:'Noviembre',12:'Diciembre'}
with st.sidebar:
    st.header('Filtros históricos')
    inicio = st.selectbox('Año inicial', anios, index=0)
    fin = st.selectbox('Año final', anios, index=len(anios)-1)
    mes_elegido = st.multiselect('Meses visibles', list(meses), default=list(meses), format_func=lambda m: meses[m])
    st.header('Parámetros de proyección')
    horizonte = st.slider('Meses a proyectar', 1, 36, 12)
    ventana = st.slider('Ventana del promedio (meses)', 2, 24, 12)
    modelo = st.selectbox('Modelo', ['Ambos','Regresión lineal','Promedio móvil'])

if inicio > fin:
    st.warning('El año inicial no puede superar el final.')
    st.stop()
if not mes_elegido:
    st.warning('Selecciona al menos un mes.')
    st.stop()
filtrado = df[df.anio.between(inicio, fin) & df.mes.isin(mes_elegido)].copy()
if filtrado.empty:
    st.warning('No hay registros para los filtros seleccionados.')
    st.stop()

st.subheader('Exploración histórica')
a, b, c, d = st.columns(4)
valores = filtrado.generacion_bruta_gwh
a.metric('Promedio mensual', f'{valores.mean():,.1f} GWh')
b.metric('Máximo mensual', f'{valores.max():,.1f} GWh')
c.metric('Mínimo mensual', f'{valores.min():,.1f} GWh')
d.metric('Total del período', f'{valores.sum():,.1f} GWh')
fig, ax = plt.subplots(figsize=(11, 3.5))
ax.plot(filtrado.fecha, valores, marker='o', markersize=2.5, linewidth=1.5)
ax.set(title='Generación bruta mensual (selección histórica)', ylabel='GWh', xlabel='Fecha')
ax.grid(alpha=.25)
fig.autofmt_xdate()
st.pyplot(fig)
plt.close(fig)

st.subheader('Proyección matemática')
st.info('Para evitar distorsiones, la proyección se entrena con TODOS los meses consecutivos hasta el año final seleccionado, independientemente del filtro de meses visibles. El año inicial y el filtro de meses solo afectan la vista histórica. El horizonte empieza después del último mes disponible de ese año.')
serie = df[df.anio <= fin].set_index('fecha')['generacion_bruta_gwh'].asfreq('MS')
if serie.isna().any():
    st.error('Hay meses faltantes en el período de entrenamiento. Revisa el dataset antes de proyectar.')
    st.stop()
if len(serie) < max(3, ventana):
    st.warning('No hay suficientes meses para la ventana elegida.')
    st.stop()
proy = proyectar(serie, horizonte, ventana, modelo)
fig2, ax2 = plt.subplots(figsize=(11, 4))
ax2.plot(serie.index, serie.values, label='Histórico completo hasta año final', color='#277da1')
for col, color in [('Regresión lineal','#43aa8b'),('Promedio móvil','#f8961e')]:
    if col in proy:
        ax2.plot([serie.index[-1], *proy.index], [serie.iloc[-1], *proy[col].tolist()], label=col, color=color, linestyle='--')
ax2.axvline(serie.index[-1], color='gray', alpha=.5)
ax2.set(title='Histórico y escenarios futuros', ylabel='GWh mensuales', xlabel='Fecha')
ax2.grid(alpha=.25)
ax2.legend()
fig2.autofmt_xdate()
st.pyplot(fig2)
plt.close(fig2)
st.dataframe(proy.rename_axis('Mes proyectado').round(2), use_container_width=True)
st.download_button('Descargar proyecciones CSV', proy.to_csv().encode('utf-8'), file_name='proyecciones_avance4.csv', mime='text/csv')

st.subheader('Comparación y confiabilidad')
metricas = evaluar_modelos(serie, ventana, prueba=12)
if metricas:
    st.write('Validación temporal: se entrenan los modelos sin los últimos 12 meses y se comparan sus predicciones con esos meses reales. Menor MAE significa menor error promedio en GWh.')
    st.dataframe(pd.DataFrame({'Modelo':list(metricas),'MAE (GWh)':list(metricas.values())}).sort_values('MAE (GWh)'), hide_index=True, use_container_width=True)
    mejor = min(metricas, key=metricas.get)
    st.success(f'En esta validación, el método con menor error fue: {mejor}. Esto no garantiza que sea el mejor en el futuro.')
else:
    st.caption('No hay suficientes datos para la validación temporal con esta configuración.')
st.warning('Limitaciones: modelos simples, sin clima, demanda, capacidad instalada ni estacionalidad explícita. No usar como pronóstico oficial ni para decisiones críticas.')
st.caption(f'Fuente: dataset incluido en el repositorio · {len(df)} registros mensuales · {df.fecha.min():%Y-%m} a {df.fecha.max():%Y-%m}.')
