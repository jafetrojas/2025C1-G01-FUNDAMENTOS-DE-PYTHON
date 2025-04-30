# Importación de librerías necesarias
import requests  # Para hacer solicitudes HTTP a la API de VirusTotal
import csv  # Para guardar los resultados en archivos CSV
from base64 import urlsafe_b64encode  # Para codificar URLs
from API_KEY import HEADERS  # Importa los encabezados con la API key desde un archivo externo
from Gráficas import graficar_resultados  # Función para graficar los resultados obtenidos
from datetime import datetime  # Para agregar fecha y hora a los registros


# Función para analizar una dirección IP
def analizar_ip(ip):
    url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip}"  # Construcción de URL para la consulta
    respuesta = requests.get(url, headers=HEADERS)  # Solicitud a la API de VirusTotal con cabeceras
    if respuesta.status_code != 200:  # Verifica si la respuesta fue exitosa
        print(" Error:", respuesta.status_code)  # Muestra el error si la solicitud falló
        return

    datos = respuesta.json()  # Convierte la respuesta JSON a un diccionario
    print(f"\n IP: {ip}")
    print(f" Reputación: {datos['data']['attributes']['reputation']}")  # Muestra la reputación
    print(f" País: {datos['data']['attributes'].get('country', 'Desconocido')}")  # País o "Desconocido"

    mostrar_resultados(datos)  # Muestra motores de análisis que detectaron problemas
    graficar_resultados(datos, ip)  # Genera una gráfica con los resultados

    reputacion = datos['data']['attributes']['reputation']
    pais = datos['data']['attributes'].get('country', 'Desconocido')

    # Guarda los resultados en un archivo CSV
    guardar_en_csv("IP", ip, reputacion, detectar_num(datos), {"pais": pais})


# Función para analizar un dominio
def analizar_dominio(dominio):
    url = f"https://www.virustotal.com/api/v3/domains/{dominio}"  # URL para consultar dominios
    respuesta = requests.get(url, headers=HEADERS)
    if respuesta.status_code != 200:
        print(" Error:", respuesta.status_code)
        return

    datos = respuesta.json()
    print(f"\n🔍 Dominio: {dominio}")
    print(f"➡️ Reputación: {datos['data']['attributes']['reputation']}")
    print(f"➡️ Registrar: {datos['data']['attributes'].get('registrar', 'Desconocido')}")
    print(f"➡️ Categoría: {datos['data']['attributes'].get('categories', 'Desconocida')}")

    mostrar_resultados(datos)
    graficar_resultados(datos, dominio)

    reputacion = datos['data']['attributes']['reputation']
    registrar = datos['data']['attributes'].get('registrar', 'Desconocido')
    categorias = ','.join(datos['data']['attributes'].get('categories', {}).keys())

    guardar_en_csv("Dominio", dominio, reputacion, detectar_num(datos), {
        "registrar": registrar,
        "categorias": categorias
    })


# Función para analizar una URL
def analizar_url(url_string):
    url_id = urlsafe_b64encode(url_string.encode()).decode().strip("=")  # Codifica la URL en base64 como exige la API
    url = f"https://www.virustotal.com/api/v3/urls/{url_id}"
    respuesta = requests.get(url, headers=HEADERS)
    if respuesta.status_code != 200:
        print(" Error:", respuesta.status_code)
        return

    datos = respuesta.json()
    print(f"\n URL: {url_string}")
    print(f"➡ Reputación: {datos['data']['attributes']['reputation']}")

    mostrar_resultados(datos)
    graficar_resultados(datos, url_string)

    reputacion = datos['data']['attributes']['reputation']
    guardar_en_csv("URL", url_string, reputacion, detectar_num(datos))


# Función para buscar un archivo a través de su hash
def buscar_por_hash(hash_val):
    url = f"https://www.virustotal.com/api/v3/files/{hash_val}"
    respuesta = requests.get(url, headers=HEADERS)
    if respuesta.status_code != 200:
        print(" Hash no encontrado o inválido")
        return

    datos = respuesta.json()
    print(f"\n Hash: {hash_val}")
    print(f"Tipo de archivo: {datos['data']['attributes'].get('type_description', 'Desconocido')}")
    print(f"️ Nombre: {datos['data']['attributes'].get('meaningful_name', 'No disponible')}")

    mostrar_resultados(datos)
    graficar_resultados(datos, hash_val)

    nombre = datos['data']['attributes'].get('meaningful_name', 'No disponible')
    tipo = datos['data']['attributes'].get('type_description', 'Desconocido')
    tamano = str(datos['data']['attributes'].get('size', '')) + " bytes"

    guardar_en_csv("Hash", hash_val, 0, detectar_num(datos), {
        "nombre_archivo": nombre,
        "tipo_archivo": tipo,
        "tamano": tamano
    })


# Función para mostrar los motores que detectaron problemas
def mostrar_resultados(datos):
    print("\n Motores que detectaron algo:")
    detectados = 0
    for motor, resultado in datos['data']['attributes']['last_analysis_results'].items():
        if resultado['category'] != 'harmless':  # Solo muestra si no es inofensivo
            print(f" - {motor}: {resultado['category']}")
            detectados += 1
    if detectados == 0:
        print("Todos los motores lo consideran seguro.")


# Función auxiliar que cuenta cuántos motores marcaron como no inofensivo
def detectar_num(datos):
    return sum(1 for r in datos['data']['attributes']['last_analysis_results'].values() if r['category'] != 'harmless')


# Función para guardar los datos en un archivo CSV
def guardar_en_csv(tipo, valor, reputacion, detectados, extra={}):
    fila = {
        "Tipo": tipo,
        "Valor": valor,
        "Reputación": reputacion,
        "Detectados": detectados,
        "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),  # Fecha y hora actual
        "País": extra.get("pais", ""),
        "Registrar": extra.get("registrar", ""),
        "Categorías": extra.get("categorias", ""),
        "NombreArchivo": extra.get("nombre_archivo", ""),
        "TipoArchivo": extra.get("tipo_archivo", ""),
        "Tamaño": extra.get("tamano", "")
    }

    archivo = "registros_de_consultas.csv"
    encabezados = fila.keys()
    try:
        with open(archivo, "a", newline='', encoding='utf-8') as f:
            escritor = csv.DictWriter(f, fieldnames=encabezados)
            if f.tell() == 0:  # Escribe encabezado si el archivo está vacío
                escritor.writeheader()
            escritor.writerow(fila)  # Escribe la fila con datos
        print(f"Resultado guardado en {archivo}")
    except Exception as e:
        print(f"Error al guardar en CSV: {e}")
