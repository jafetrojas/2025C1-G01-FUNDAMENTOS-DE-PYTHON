"""
Autor: Jafet Rojas
Fecha: 16/04/2025
versión: 0.1
Sistema de Gestión de Ventas que nos permita ingresar, almacenar y analizar datos de ventas.  
"""
import os 
from modulo import ingresar_ventas, guardar_ventas, analisis_ventas


#lIMPIA PANTALLA DE TERMINAL

def limpiar_pantalla():
    """Limpia la pantalla de la terminal en ejecución"""
    os.system('cls' if os.name == 'nt' else 'clear')


def pausar():
    input(" Presione Enter para continuar....")
#Menu principal

def menu():
    ventas = []
    while True:
        print("--- Menú Principal --- ")
        print("1. Ingresar ventas de cursos UMCA")
        print("2. Guardar datos en un archivo CSV")
        print("3. Analizar las ventas")
        print("4. Salir")
        opcion = int(input("Ingrese un opción: "))
        
        if opcion == 1:
            limpiar_pantalla()
            print("---- Ingreso de ventas de cursos  millonarios --- ")
            ingresar_ventas(ventas)
            pausar()
        elif opcion == 2:
            limpiar_pantalla()
            print("--- Guardar Ventas en CSV--- ")
            guardar_ventas(ventas)
            pausar()
        elif opcion == 3:
            limpiar_pantalla()
            print(" --- Análisis de Ventas --- ")
            analisis_ventas()
            pausar()
        elif opcion == 4:
            print("*** Gracias por usar el sistema. SEE YOU! *** ")
            pausar()
            break
        else:
            print("Opción no valida. Intente nuevamente una opción ")
            pausar()
            
            
#Ejecución del sistema solo si el archivo que yo estoy llamando sea el MAIN.
if __name__ == "__main__":
    print("Bienvenido al sistema de Gestión de Ventas")
    menu()
