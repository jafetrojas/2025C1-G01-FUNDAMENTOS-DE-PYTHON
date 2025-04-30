# Importamos pandas para análisis de datos y datetime para manejar fechas
import pandas as pd

# Cargamos el archivo CSV con los registros
archivo = "registros_de_consultas.csv"
df = pd.read_csv(archivo)

# Convertimos la columna 'Fecha' a tipo datetime para ordenarla correctamente
df['Fecha'] = pd.to_datetime(df['Fecha'])

# --- 1. Ver los 5 registros más recientes ---
print("\n Últimos 5 registros (más recientes primero):")
print(df.sort_values(by="Fecha", ascending=False).head())

# --- 2. Mostrar el elemento con más detecciones ---
print("\n Elemento con más motores que detectaron amenaza:")
print(df.sort_values(by="Detectados", ascending=False).head(1))

# --- 3. Cantidad de consultas por tipo (IP, Dominio, etc.) ---
print("\n Conteo de registros por tipo de análisis:")
print(df["Tipo"].value_counts())

# --- 4. Promedio de reputación por tipo de análisis ---
print("\n Reputación promedio por tipo:")
print(df.groupby("Tipo")["Reputación"].mean())

# --- 5. Primer registro hecho (cronológicamente) ---
print("\n Primer análisis registrado:")
print(df.sort_values(by="Fecha").head(1))

# --- 6. Países con más detecciones acumuladas ---
print("\n Países con más detecciones (acumuladas):")
print(df.groupby("País")["Detectados"].sum().sort_values(ascending=False))