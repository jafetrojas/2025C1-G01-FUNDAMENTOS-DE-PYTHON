

# archivo: analizador_pcap.py

import pyshark
import os
import statistics
import matplotlib.pyplot as plt
from collections import Counter

# Variables globales
data_summary = {}
file_path = ""
packet_list = []
unique_ips = set()

def cargar_pcap():
    global file_path, packet_list, unique_ips
    file_path = "C:/Users/Usuario/Downloads/Instrucciones Examen (1)/academia_Ciberseguridad2025.pcapng"
    if not os.path.exists(file_path):
        print("Archivo 'academia_Ciberseguridad2025.pcapng' no encontrado. Asegúrese de que el archivo esté en el mismo directorio que este script.")
        return False
    try:
        print("Cargando archivo...")
        capture = pyshark.FileCapture(file_path, only_summaries=True)
        packet_list = list(capture)
        capture.close()
        print(f"Archivo cargado exitosamente: {len(packet_list)} paquetes encontrados.")
        return True
    except Exception as e:
        print(f"Error al cargar el archivo: {e}")
        return False

def mostrar_resumen():
    global data_summary
    total_packets = len(packet_list)
    protocols = {}
    ip_counter = {}
    for pkt in packet_list:
        proto = pkt.protocol
        protocols[proto] = protocols.get(proto, 0) + 1

        src = pkt.source
        dst = pkt.destination
        if src and dst:
            unique_ips.update([src, dst])
            ip_counter[src] = ip_counter.get(src, 0) + 1
            ip_counter[dst] = ip_counter.get(dst, 0) + 1

    top_ip = max(ip_counter, key=ip_counter.get) if ip_counter else "N/A"
    top_proto = max(protocols, key=protocols.get) if protocols else "N/A"

    data_summary = {
        "Total de paquetes": total_packets,
        "Protocolos detectados": protocols,
        "IP más activa": top_ip,
        "Protocolo más usado": top_proto
    }

    print("\n--- Resumen General ---")
    for k, v in data_summary.items():
        print(f"{k}: {v}")

    visualizar_protocolos(protocols)

def visualizar_protocolos(protocols):
    if not protocols:
        return
    labels, counts = zip(*Counter(protocols).most_common(5))
    plt.figure(figsize=(8, 5))
    plt.bar(labels, counts, color='skyblue')
    plt.title("Top 5 Protocolos por Frecuencia")
    plt.xlabel("Protocolo")
    plt.ylabel("Cantidad de paquetes")
    plt.tight_layout()
    plt.show()

def filtrar_por_ip():
    ip = input("Ingrese la IP para filtrar: ")
    print(f"\nPaquetes donde participa la IP {ip}:")
    encontrados = 0
    for pkt in packet_list:
        if pkt.source == ip or pkt.destination == ip:
            print(pkt)
            encontrados += 1
    print(f"\nTotal: {encontrados} paquetes encontrados.")

def buscar_por_protocolo():
    proto = input("Ingrese el nombre del protocolo (ej. TCP, UDP, DNS): ").upper()
    encontrados = [pkt for pkt in packet_list if pkt.protocol == proto]
    print(f"\n{len(encontrados)} paquetes encontrados con protocolo {proto}.")
    for pkt in encontrados[:10]:
        print(pkt)

def detectar_anomalias():
    ip_counter = Counter()
    for pkt in packet_list:
        src = pkt.source
        if src:
            ip_counter[src] += 1
    sospechosas = [ip for ip, count in ip_counter.items() if count > 100]
    print("\n--- IPs con tráfico sospechoso (más de 100 paquetes) ---")
    for ip in sospechosas:
        print(f"{ip} - {ip_counter[ip]} paquetes")
    if not sospechosas:
        print("No se detectaron IPs sospechosas.")
