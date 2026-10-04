import logging
import time

import streamlit as st

from processor import PacketProcessor
from sniffer import start_sniffing
from visualizations import create_visualizations

logging.basicConfig(
    filename='app_red.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

st.set_page_config(page_title='Análisis de Tráfico de Red', layout='wide')


@st.cache_resource
def get_processor():
    """Se crea UNA sola vez por proceso (no por cada rerun ni por cada pestaña)."""
    processor = PacketProcessor()
    processor.start_time = time.time()
    start_sniffing(processor)
    return processor


@st.fragment(run_every=2)
def dashboard(processor):
    df = processor.get_dataframe()

    if processor.error:
        st.error(
            f'El sniffer no pudo capturar paquetes: {processor.error}\n\n'
            'Ejecutá con permisos de administrador/root (y en Windows '
            'instalá Npcap).'
        )

    col1, col2 = st.columns(2)
    col1.metric('Total de Paquetes', processor.total_captured)
    col2.metric(
        'Tiempo Transcurrido', f'{time.time() - processor.start_time:.0f}s'
    )

    create_visualizations(df)

    st.subheader('Últimos Paquetes Capturados')
    if df.empty:
        st.info('Esperando que caigan paquetes de red...')
    else:
        st.dataframe(df.tail(10))


def main():
    st.title('📡 Análisis de Tráfico de Red en Tiempo Real')
    dashboard(get_processor())


if __name__ == '__main__':
    main()
