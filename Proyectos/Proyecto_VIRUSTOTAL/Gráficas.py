# Importamos la librería matplotlib para generar gráficas
import matplotlib.pyplot as plt

# Función que genera una gráfica de barras con los resultados del análisis
def graficar_resultados(datos, nombre_objeto):
    detecciones = {}  # Diccionario para almacenar los motores que detectaron algo

    # Recorremos los resultados de los motores de análisis
    for motor, resultado in datos['data']['attributes']['last_analysis_results'].items():
        categoria = resultado['category']  # Obtenemos la categoría del resultado

        # Traducción de categorías técnicas a descripciones en español más comprensibles
        if categoria == 'undetected':
            categoria_traducida = 'No detectaron amenaza'
        elif categoria in ['malicious', 'suspicious', 'detected']:
            categoria_traducida = 'Detectaron amenaza'
        elif categoria == 'timeout':
            categoria_traducida = 'No respondió (timeout)'
        elif categoria == 'type-unsupported':
            categoria_traducida = 'Tipo no compatible'
        elif categoria == 'failure':
            categoria_traducida = 'Fallo en el análisis'
        else:
            categoria_traducida = 'Categoría desconocida'

        # Solo agregamos motores cuyo resultado no sea 'harmless'
        if categoria != 'harmless':
            detecciones[motor] = categoria_traducida

    # Si no hay detecciones, no se genera la gráfica
    if not detecciones:
        print(" Nada que graficar. Todo limpio.")
        return

    # Contamos cuántos motores cayeron en cada categoría traducida
    categorias = list(detecciones.values())
    conteo = {}
    for cat in categorias:
        conteo[cat] = conteo.get(cat, 0) + 1  # Acumula el conteo por categoría

    # Separamos las claves (categorías) y sus valores (número de motores)
    claves = list(conteo.keys())
    valores = list(conteo.values())
    total = sum(valores)  # Total de motores que detectaron algo

    # Para evitar errores en matplotlib si hay solo una barra, duplicamos los datos
    if len(claves) == 1:
        claves.append(claves[0])
        valores.append(valores[0])

    # Elegimos un color según la cantidad total de detecciones
    color = 'darkred' if total > 5 else 'green'

    # Configuración de la gráfica de barras
    plt.figure(figsize=(8, 4))  # Tamaño de la figura
    plt.bar(claves, valores, color=color)  # Crea barras por categoría
    plt.xticks(rotation=40)  # Gira las etiquetas del eje X para mejor visibilidad
    plt.title(f"{total} Total de detecciones con: {nombre_objeto}")  # Título de la gráfica
    plt.xlabel("Categoría")  # Etiqueta del eje X
    plt.ylabel("Cantidad de motores")  # Etiqueta del eje Y

    # Añade los valores sobre las barras
    for i, v in enumerate(valores):
        plt.text(i, v + 0.1, str(v), ha='center')  # Posiciona el texto centrado sobre la barra

    # Añade una cuadrícula ligera al fondo
    plt.grid(True, axis='y', linestyle='--', alpha=0.5)

    # Ajusta el diseño para evitar superposición
    plt.tight_layout()

    # Muestra la gráfica
    plt.show()