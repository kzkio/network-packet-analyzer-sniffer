import plotly.express as px
import streamlit as st


def protocol_distribution(df):
    fig = px.histogram(
        df, x='protocol', color='protocol', title='Distribución de Protocolos'
    )
    st.plotly_chart(fig)


def traffic_over_time(df):
    per_sec = (
        df.set_index('timestamp')['size'].resample('1s').sum().reset_index()
    )
    fig = px.line(
        per_sec,
        x='timestamp',
        y='size',
        title='Tráfico en el tiempo (bytes por segundo)',
    )
    st.plotly_chart(fig)


def top_sources(df, n: int = 10):
    top = df['source'].value_counts().head(n).reset_index()
    top.columns = ['source', 'paquetes']
    fig = px.bar(top, x='source', y='paquetes', title=f'Top {n} IPs de origen')
    st.plotly_chart(fig)


def create_visualizations(df):
    if df.empty:
        return
    col1, col2 = st.columns(2)
    with col1:
        protocol_distribution(df)
    with col2:
        top_sources(df)
    traffic_over_time(df)
