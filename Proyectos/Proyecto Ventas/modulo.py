#Poner funciones que quiera utilizar.
import csv, os, pandas as pd


def ingresar_ventas(lista_ventas):
    while True:
        try:
            curso = input("Por favor ingrese el nombre del curso: ").upper()
            cantidad = int(input("Ingrese la cantidad de cursos vendidos: "))
            fecha = input("Ingrese la fecha de la venta (año-mes-dia: )")
            precio = float(input("Ingrese el precio del curso: "))
            cliente = input('Ingrese el nombre del cliente: ').upper()
        except ValueError:
            print("Entradas no validas, intente nuevamente")
            continue
        
        venta =  {
            "curso" : curso,
            "cantidad" : cantidad,
            "precio" : precio,
            "fecha" : fecha,
            "cliente" : cliente,
            
        }
        lista_ventas.append(venta)
        
        continuar = input("Desea Ingresar otra Venta s/n : ").lower()
        if continuar == "s":
            print(" ---- Ingresando Otra Venta ----")
        elif continuar == "n":
            break
        else:
            print ("Opción no valida")
            
            
            
#def guardar_ventas(ventas):
    #if not ventas:
        #print("Hoy no hay ventas que guardar en el CSV")
    #else:
        #with open("ventas.csv", "w" , newline="",enconding= "utf-8" ) as archivo:
            #guardar = csv.DictWriter(archivo,fieldnames=["curso", "cantidad", "precio", "fecha", "cliente"])
            #guardar.writeheader()
            #guardar.writerows(ventas)
        #print("Datos Guardados de manera exitosa")
        
def guardar_ventas(ventas):
    if not ventas:
        print('No hay ventas que guardar en el CSV')
    else:
        if os.path.exists('ventas.csv'):
            #si el archivo existe agrego Append 'A'
            with open('ventas.csv','a',newline='',encoding='utf-8') as archivo:
                guardar = csv.DictWriter(archivo,fieldnames=['curso','cantidad','precio','fecha','cliente'])
                guardar.writerows(ventas)        
        else: #Si no existe abro en modo escritura 'W'
            with open('ventas.csv','w',newline='',encoding='utf-8') as archivo:
                guardar = csv.DictWriter(archivo,fieldnames=['curso','cantidad','precio','fecha','cliente'])
                guardar.writeheader()
                guardar.writerows(ventas)
                
        #Limpio las ventas en memoria y muestro el guardado exitoso
        ventas = []
        print('Datos guardados exitosamente!')
        
def analisis_ventas():
    df = pd.read_csv("ventas.csv")
    print("---------------------- RESUMEN VENTAS -------------------")
    
    df["subtotal"] = df["cantidad"] * df["precio"]
    total_ingresos = df["subtotal"].sum()
    
    print(f"total de ventas{total_ingresos}")
    
    #mas vendido
    curso_top = df.groupby("curso")["cantidad"].sum().idxmax()
    print("El curso más vendido es: ", curso_top)
    
    #el que compro mas cursos
    comprador_top = df.groupby("cliente")["cantidad"].sum().idxmax()
    print("la persona que mas compro cursos es: ", comprador_top)
    # Ordenando de forma ascendente
    ventas_enorden = df.sort_values("fecha", ascending=True)  
    print(ventas_enorden[["fecha", "cliente", "curso", "cantidad"]].to_string(index=False))
   