import streamlit as st
import pandas as pd
import requests
import io
import time

# 1. Configurazione Pagina
st.set_page_config(page_title="Rally Live Sulcis", layout="wide")

# 2. Identificativi
FILE_ID = "1wjiKfefjCsiCuqkuu74DP2iCo9VHoNaf"
# URL diretto per il download senza parametri che disturbano il server
CSV_URL = f"https://docs.google.com/spreadsheets/d/{FILE_ID}/export?format=csv"

# 3. Funzione di recupero dati
def fetch_rally_data():
    try:
        # Download tramite requests per bypassare limitazioni di pandas
        response = requests.get(CSV_URL, timeout=10)
        
        # Se il server risponde con errore (es. 403 o 404), viene generata un'eccezione
        response.raise_for_status()
        
        # Lettura del contenuto CSV in memoria
        return pd.read_csv(io.BytesIO(response.content))
    
    except requests.exceptions.HTTPError as e:
        if "400" in str(e):
            st.error("❌ Errore 400: Richiesta malformata. Verifica l'ID del file.")
        elif "403" in str(e):
            st.error("❌ Errore 403: Accesso Negato. Imposta il file su Drive come 'PUBBLICO'.")
        else:
            st.error(f"⚠️ Errore Server: {e}")
        return None
    except Exception as e:
        st.error(f"📡 Errore Connessione: {e}")
        return None

# 4. Interfaccia Utente
st.title("⏱️ Rally Live Sulcis - PS10")

data_frame = fetch_rally_data()

if data_frame is not None and not data_frame.empty:
    # Mostra i primi 3 classificati
    cols = st.columns(3)
    titles = ["🥇 1° Posto", "🥈 2° Posto", "🥉 3° Posto"]
    for i, col in enumerate(cols):
        if len(data_frame) > i:
            col.metric(titles[i], data_frame.iloc[i]['Pilota'])

    st.divider()

    # Tabella principale
    st.subheader("Classifica in tempo reale")
    st.dataframe(data_frame, use_container_width=True, hide_index=True)
    
    st.caption(f"Ultimo aggiornamento: {time.strftime('%H:%M:%S')}")
else:
    st.warning("In attesa di dati validi da Google Drive...")

# 5. Logica Refresh (25 secondi)
time.sleep(25)
st.rerun()
