import streamlit as st
import pandas as pd
import time
import random

# 1. Configurazione della pagina (Deve essere la prima istruzione Streamlit)
st.set_page_config(
    page_title="Rally Live Sulcis - PS10",
    page_icon="⏱️",
    layout="wide"
)

# 2. Parametri di configurazione
FILE_ID = "1wjiKfefjCsiCuqkuu74DP2iCo9VHoNaf"
# URL pulito per l'esportazione CSV
BASE_URL = f"https://docs.google.com/spreadsheets/d/{FILE_ID}/export?format=csv"

# 3. Funzione di caricamento dati ottimizzata
def load_data():
    # Usiamo il timestamp come parametro per il cache-busting (evita l'errore 400)
    timestamp = int(time.time())
    full_url = f"{BASE_URL}&t={timestamp}"
    
    try:
        # Caricamento con User-Agent per simulare un browser ed evitare blocchi
        data = pd.read_csv(full_url, storage_options={'User-Agent': 'Mozilla/5.0'})
        return data
    except Exception as e:
        # Mostra l'errore tecnico solo in debug, altrimenti un messaggio pulito
        st.error(f"Connessione a Google Drive interrotta. Riprovo... (Dettaglio: {e})")
        return None

# 4. Interfaccia Utente (UI)
st.title("🏁 Rally Live Sulcis - Classifica PS10")

# Banner scorrevole (CSS)
st.markdown("""
    <style>
    .marquee {
        width: 100%; line-height: 40px; background-color: #ff4b4b; color: white;
        white-space: nowrap; overflow: hidden; box-sizing: border-box; font-weight: bold;
    }
    .marquee p {
        display: inline-block; padding-left: 100%; animation: marquee 20s linear infinite; margin: 0;
    }
    @keyframes marquee {
        0% { transform: translate(0, 0); }
        100% { transform: translate(-100%, 0); }
    }
    </style>
    <div class="marquee"><p>AGGIORNAMENTO LIVE OGNI 30 SECONDI - CLASSIFICA PROVVISORIA PROVA SPECIALE 10</p></div>
    """, unsafe_allow_html=True)

# Spazio verticale
st.write("")

# Caricamento effettivo
df = load_data()

if df is not None and not df.empty:
    # Mostra i primi 3 come metriche principali
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🥇 1° Posto", df.iloc[0]['Pilota'], "Leader")
    with col2:
        dist2 = df.iloc[1]['Distacco'] if 'Distacco' in df.columns else ""
        st.metric("🥈 2° Posto", df.iloc[1]['Pilota'], f"+{dist2}")
    with col3:
        dist3 = df.iloc[2]['Distacco'] if 'Distacco' in df.columns else ""
        st.metric("🥉 3° Posto", df.iloc[2]['Pilota'], f"+{dist3}")

    st.divider()

    # Tabella completa aggiornata
    st.subheader("Classifica Completa")
    st.dataframe(
        df, 
        use_container_width=True, 
        hide_index=True,
        column_config={
            "Pos": "Posizione",
            "N": "N°",
            "Tempo": "⏱️ Tempo",
            "Distacco": "Gap"
        }
    )
    
    st.caption(f"Ultimo controllo: {time.strftime('%H:%M:%S')}")
else:
    st.info("🔄 Ricezione dati in corso... Assicurati che il file su Drive sia 'Pubblico' e che Colab sia attivo.")

# 5. Logica di Refresh (30 secondi come concordato)
time.sleep(30)
st.rerun()
