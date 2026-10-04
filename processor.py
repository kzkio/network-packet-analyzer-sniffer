import logging
import threading
from collections import deque
from datetime import datetime

import pandas as pd
from scapy.layers.inet import ICMP, IP, TCP, UDP
from scapy.layers.inet6 import IPv6
from scapy.layers.l2 import ARP, Ether

logger = logging.getLogger(__name__)


class PacketProcessor:
    """Recibe paquetes desde el sniffer (otro hilo) y los guarda de forma segura."""

    def __init__(self, max_packets: int = 5000):
        self._packets = deque(maxlen=max_packets)
        self._lock = threading.Lock()
        self.total_captured = 0
        self.error = None  # si el sniffer falla, acá queda el mensaje

    @staticmethod
    def _protocol(packet) -> str:
        if packet.haslayer(TCP):
            return 'TCP'
        if packet.haslayer(UDP):
            return 'UDP'
        if packet.haslayer(ICMP):
            return 'ICMP'
        if packet.haslayer(ARP):
            return 'ARP'
        if packet.haslayer(IPv6):
            return 'IPv6'
        return 'Otro'

    @staticmethod
    def _addresses(packet):
        if packet.haslayer(IP):
            return packet[IP].src, packet[IP].dst
        if packet.haslayer(IPv6):
            return packet[IPv6].src, packet[IPv6].dst
        if packet.haslayer(ARP):
            return packet[ARP].psrc, packet[ARP].pdst
        if packet.haslayer(Ether):
            return packet[Ether].src, packet[Ether].dst
        return 'desconocido', 'desconocido'

    def process_packet(self, packet) -> None:
        try:
            src, dst = self._addresses(packet)
            record = {
                'timestamp': datetime.now(),
                'source': src,
                'destination': dst,
                'protocol': self._protocol(packet),
                'size': len(packet),
            }
            with self._lock:
                self._packets.append(record)
                self.total_captured += 1
        except Exception:
            logger.exception('Error procesando paquete')

    def get_dataframe(self) -> pd.DataFrame:
        with self._lock:
            data = list(self._packets)
        return pd.DataFrame(
            data,
            columns=['timestamp', 'source', 'destination', 'protocol', 'size'],
        )
