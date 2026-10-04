# 📡 Dashboard de Tráfico de Red en Tiempo Real

Aplicación que captura paquetes de red con **Scapy** y los muestra en un dashboard
interactivo hecho con **Streamlit** y **Plotly**, que se actualiza solo cada 2 segundos.

> Basado en el tutorial de freeCodeCamp:
> [Build a Real-Time Network Traffic Dashboard with Python and Streamlit](https://www.freecodecamp.org/news/build-a-real-time-network-traffic-dashboard-with-python-and-streamlit/).
> Reorganicé el código en módulos y lo modifiqué (ver "Cambios respecto al tutorial").

## Qué muestra

- Total de paquetes capturados y tiempo transcurrido
- Distribución de protocolos (TCP, UDP, ICMP, ARP, IPv6)
- Top 10 IPs de origen
- Tráfico en el tiempo (bytes por segundo)
- Tabla con los últimos paquetes capturados

## Estructura

| Archivo | Rol |
|---|---|
| `app.py` | Interfaz de Streamlit y refresco automático |
| `processor.py` | Clase `PacketProcessor`: procesa y almacena paquetes (thread-safe) |
| `sniffer.py` | Captura de paquetes en un hilo aparte |
| `visualizations.py` | Gráficos de Plotly |

## Requisitos

- Python 3.9+
- **Windows:** [Npcap](https://npcap.com) instalado
- **Linux/Mac:** permisos de root para capturar

## Instalación y uso

```bash
git clone <url-del-repo>
cd <carpeta>
python -m venv venv
venv\Scripts\activate        # en Linux/Mac: source venv/bin/activate
pip install -r requirements.txt
python -m streamlit run app.py
```

⚠️ La captura de paquetes requiere **permisos de administrador**: abrí la terminal
como administrador (Windows) o usá `sudo` con el Streamlit de tu entorno virtual
(Linux/Mac). Si faltan permisos, la app muestra el error en pantalla.

## Cambios respecto al tutorial

- Código separado en módulos en vez de un solo archivo
- Un único sniffer compartido (`st.cache_resource`) en vez de uno por sesión
- Refresco con `st.fragment(run_every=2)` en lugar de `sleep` + `rerun`
- Manejo de errores del sniffer visible en la interfaz
- Gráficos adicionales (top IPs y tráfico en el tiempo)

## Aviso

Usalo únicamente para analizar **tu propia red** o redes en las que tengas
autorización. Capturar tráfico ajeno sin permiso puede ser ilegal.
