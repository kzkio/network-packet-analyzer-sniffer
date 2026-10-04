import logging
import threading

from scapy.all import sniff

logger = logging.getLogger(__name__)


def start_sniffing(processor, iface=None) -> threading.Thread:
    """Arranca la captura en un hilo aparte para no bloquear Streamlit."""

    def _run():
        try:
            sniff(prn=processor.process_packet, store=False, iface=iface)
        except Exception as e:
            # Lo más común: falta de permisos (admin/root) o Npcap no instalado
            processor.error = f'{type(e).__name__}: {e}'
            logger.exception('El sniffer se detuvo')

    thread = threading.Thread(target=_run, daemon=True, name='sniffer')
    thread.start()
    return thread
