# archivo: main.py

from modulo import (
    cargar_pcap,
    mostrar_resumen,
    filtrar_por_ip,
    buscar_por_protocolo,
    detectar_anomalias
)

def menu_principal():
    if not cargar_pcap():
        return

    while True:
        print("\n--- Menú Principal ---")
        print("1. Ver resumen general")
        print("2. Filtrar por IP")
        print("3. Buscar por protocolo")
        print("4. Detectar conexiones sospechosas")
        print("5. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            mostrar_resumen()
        elif opcion == "2":
            filtrar_por_ip()
        elif opcion == "3":
            buscar_por_protocolo()
        elif opcion == "4":
            detectar_anomalias()
        elif opcion == "5":
            print("Saliendo del programa.")
            break
        else:
            print("Opción inválida. Intente nuevamente.")

if __name__ == "__main__":
    menu_principal()
