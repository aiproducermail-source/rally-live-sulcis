import streamlit as st
import pandas as pd
import requests
import io
import time
from datetime import datetime

# 1. CONFIGURAZIONE ESTETICA (Racing Theme)
st.set_page_config(
    page_title="Rally Live Sulcis - Pro",
    page_icon="🏎️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS per migliorare l'aspetto (Colori Racing)
st.markdown("""
    <style>
    .main { background-color: #0f172a; }
    .stMetric { background-color: #1e293b; padding: 15px; border-radius: 10px; border-left: 5px solid #fbbf24; }
    div[data-testid="stMetricValue"] { color: #fbbf24; font-family: 'Courier New', monospace; }
    .stDataFrame { border: 1px solid #334155; border-radius: 10px; }
    h1 { color: #fbbf24 !important; text-transform: uppercase; letter-spacing: 2px; }
    .status-box { padding: 10px; border-radius: 5px; background-color: #334155; color: #38bdf8; font-size: 0.8rem; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# 2. CONFIGURAZIONE DATI
FILE_ID = "1wjiKfefjCsiCuqkuu74DP2iCo9VHoNaf"
CSV_URL = f"https://drive.google.com/uc?export=download&id={FILE_ID}&confirm=t"

def fetch_data():
    try:
        session = requests.Session()
        response = session.get(CSV_URL, timeout=10)
        response.raise_for_status()
        df = pd.read_csv(io.BytesIO(response.content))
        # Pulizia nomi colonne per sicurezza
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        return None

# 3. HEADER DASHBOARD
col_head1, col_head2 = st.columns([3, 1])
with col_head1:
    st.title("⏱️ RALLY LIVE SULCIS 2026")
    st.subheader("PROVA SPECIALE 10 - CLASSIFICA IN TEMPO REALE")

with col_head2:
    st.write("")
    st.markdown(f'<div class="status-box">Sincronizzazione: {datetime.now().strftime("%H:%M:%S")}</div>', unsafe_allow_html=True)

# 4. LOGICA DISPLAY
df = fetch_data()

if df is not None and not df.empty:
    # PODIO (TOP 3)
    st.write("### 🏆 LEADERS PS10")
    m1, m2, m3 = st.columns(3)
    
    # Estrazione sicura dei dati
    def get_val(idx, col):
        return df.iloc[idx][col] if len(df) > idx else "---"

    m1.metric("🥇 1° POSTO", get_val(0, 'Pilota'), "LEADER", delta_color="normal")
    m2.metric("🥈 2° POSTO", get_val(1, 'Pilota'), f"+{get_val(1, 'Distacco')}")
    m3.metric("🥉 3° POSTO", get_val(2, 'Pilota'), f"+{get_val(2, 'Distacco')}")

    st.divider()

    # TABELLA DETTAGLIATA
    st.write("### 📋 CLASSIFICA COMPLETA")
    
    # Formattazione colonne
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Pos": st.column_config.NumberColumn("POS", format="%d"),
            "N": "N°",
            "Pilota": "EQUIPAGGIO",
            "Tempo": "TEMPO PS",
            "Distacco": "GAP"
        }
    )
    
    # Progress Bar simbolica
    st.progress(len(df) / 50 if len(df) < 50 else 1.0, text=f"Equipaggi arrivati: {len(df)}")

else:
    st.warning("🔄 Collegamento al server in corso... La classifica verrà visualizzata non appena i dati saranno disponibili su Drive.")
    st.info("Nota: Assicurati che lo script su Google Colab sia in esecuzione.")

# 5. REFRESH AUTOMATICO (25 secondi)
time.sleep(25)
st.rerun()
