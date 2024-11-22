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