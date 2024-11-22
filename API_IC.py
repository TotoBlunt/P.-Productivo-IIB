import streamlit as st
import requests
from supabase import create_client,Client

#Configuracion de la configuracion a supabase
SUPABASE_URL = "https://nvfwifjeceexhwaknvnx.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im52ZndpZmplY2VleGh3YWtudm54Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzIyNDEzMTAsImV4cCI6MjA0NzgxNzMxMH0.9K6DaGQF9JZD_-_jCPQXbRkprV0uXFcJp9ML-a6MMW8"
supabase: Client = create_client(SUPABASE_URL,SUPABASE_KEY)

#Consumir API de tipo de cambio
def get_exchange_rate(base_currency="USD",target_currency="EUR"):
    url =f"https://api.exchangerate.host/latest?base={base_currency}&symbols={target_currency}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return{"error":"Nose puede conectar al API"}
    
# Guardar los dtos en supabase
def save_to_supabase(data):
    response = supabase.table("exchange_rates").insert(data).execute()
    return response

#Interfaz con streamlit
st.title("Consulta y Registro de tipo de cambio")

#Seleccionar las monedas
base_currency = st.selectbox("Moneda Base", ["USD","EUR","PEN"])
target_currency = st.selectbox("Moneda Objetivo", ["USD","EUR","PEN"])

#Consultar el tipo de cambio
if st.button("Consultar tipo de cambio"):
    exchange_rate_data = get_exchange_rate(base_currency,target_currency)
    if "error" in exchange_rate_data:
        st.error(exchange_rate_data['error'])
    else:
        rate = exchange_rate_data['rates'][target_currency]
        st.success(f'1 {base_currency} = {rate} {target_currency}')

    #Espacio para anotar comentarios
    comment = st.text_area("Escribe un comentario sobre esta consulta: ")

    if st.button("Guardar en supabase"):
        data_to_save = {
            "base_currency" : base_currency,
            "target_currency" : target_currency,
            "exchange_rate" : rate,
            "comment" : comment
        }

        response = save_to_supabase(data_to_save)
        if response.status == 201:
            st.sucess("Datos guardados en el supabase")
        else:
            st.error("Error al guardar los datos en supabase")