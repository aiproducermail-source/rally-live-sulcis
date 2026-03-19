import streamlit as st
import pandas as pd
import time
import random

# Configurazione Pagina
st.set_page_config(page_title="Rally Live Sulcis", layout="wide")

FILE_ID = "1wjiKfefjCsiCuqkuu74DP2iCo9VHoNaf"
URL = f"https://docs.google.com/spreadsheets/d/{FILE_ID}/export?format=csv"

def load_data():
    # Cache busting per forzare il download del nuovo file da Drive
    nocache = random.randint(1, 100000)
    full_url = f"{URL}&v={nocache}"
    try:
        return pd.read_csv(full_url)
    except Exception as e:
        st.error(f"Errore di connessione a Google Drive: {e}")
        return None

# UI Dashboard
st.title("⏱️ Live PS10 - Rally Sulcis")

df = load_data()

if df is not None and not df.empty:
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.caption(f"Ultimo aggiornamento dati: {time.strftime('%H:%M:%S')}")
else:
    st.warning("In attesa di dati da Google Drive... Verifica che il file sia condiviso come 'Pubblico'.")

# Sistema di auto-refresh sicuro ogni 25 secondi
time.sleep(25)
st.rerun()
