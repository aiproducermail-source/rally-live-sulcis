import streamlit as st
import pandas as pd
import requests
import io
import time

# 1. Configurazione Pagina
st.set_page_config(page_title="Rally Live Sulcis", layout="wide")

# ID estratto dal tuo link
FILE_ID = "1wjiKfefjCsiCuqkuu74DP2iCo9VHoNaf"

# URL specifico per il download diretto di file caricati (non Google Sheets)
CSV_URL = f"https://drive.google.com/uc?export=download&id={FILE_ID}&confirm=t"

def fetch_rally_data():
    try:
        # Sessione per gestire eventuali cookie di sicurezza di Google
        session = requests.Session()
        response = session.get(CSV_URL, timeout=10)
        response.raise_for_status()
        
        # Caricamento dati
        return pd.read_csv(io.BytesIO(response.content))
    except Exception as e:
        st.error(f"⚠️ Errore di sincronizzazione: {e}")
        st.info("Verifica che il file su Drive abbia 'Accesso generale: Chiunque abbia il link'.")
        return None

# --- Interfaccia Grafica ---
st.title("🏁 Rally Live Sulcis - PS10")

df = fetch_rally_data()

if df is not None:
    # Top 3 Metrics
    cols = st.columns(3)
    for i in range(min(3, len(df))):
        nome = df.iloc[i]['Pilota'] if 'Pilota' in df.columns else "N/D"
        cols[i].metric(f"{i+1}° Posizione", nome)
    
    st.divider()
    
    # Tabella Classifica
    st.subheader("Classifica Completa")
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.caption(f"Ultimo aggiornamento: {time.strftime('%H:%M:%S')}")
else:
    st.warning("In attesa di connessione con il database di gara...")

# Refresh automatico ogni 30 secondi
time.sleep(30)
st.rerun()
