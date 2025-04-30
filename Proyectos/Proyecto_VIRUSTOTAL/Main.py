
print("Proyecto de JAFET ROJAS ZAMORA")

# Importamos las funciones de análisis desde el archivo Funciones.py
from Funciones import analizar_ip, analizar_dominio, analizar_url, buscar_por_hash

# Definimos la función principal del menú
def menu():
    while True:  # Bucle infinito que se detiene solo si el usuario elige salir
        # Mostramos las opciones disponibles al usuario
        print("\n--- MENÚ ANÁLISIS DE VIRUS ---")
        print("1. Analizar IP")
        print("2. Analizar Dominio")
        print("3. Analizar URL")
        print("4. Buscar por Hash")
        print("5. Salir")

        # Solicitamos al usuario que seleccione una opción
        opcion = input("Seleccione una opción: ")

        # Evaluamos la opción ingresada y llamamos a la función correspondiente
        if opcion == "1":
            ip = input("IP a analizar: ")  # Pedimos la IP al usuario
            analizar_ip(ip)  # Ejecutamos el análisis de IP
        elif opcion == "2":
            dominio = input("Dominio a analizar: ")  # Pedimos el dominio
            analizar_dominio(dominio)  # Ejecutamos el análisis de dominio
        elif opcion == "3":
            url = input("URL a analizar: ")  # Pedimos la URL
            analizar_url(url)  # Ejecutamos el análisis de URL
        elif opcion == "4":
            hash_val = input("Ingrese el hash del archivo: ")  # Pedimos el hash del archivo
            buscar_por_hash(hash_val)  # Ejecutamos la búsqueda por hash
        elif opcion == "5":
            print(" Gracias por ser de su preferencia. ")  # Mensaje de despedida
            break  # Salimos del bucle y finaliza el programa
        else:
            print("Opción inválida. Intente de nuevo.")  # Mensaje de error para opciones no válidas

# Punto de entrada del programa: ejecuta el menú solo si el archivo se ejecuta directamente
if __name__ == "__main__":
    menu()