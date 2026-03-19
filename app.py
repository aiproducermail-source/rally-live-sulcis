import streamlit as st
import pandas as pd
import time
import random

FILE_ID = "1wjiKfefjCsiCuqkuu74DP2iCo9VHoNaf"
URL = f"https://docs.google.com/spreadsheets/d/1wjiKfefjCsiCuqkuu74DP2iCo9VHoNaf/export?format=csv"

st.set_page_config(page_title="Rally Live", layout="wide")

# Funzione di lettura con "Cache Busting" per evitare dati vecchi
def load_data():
    nocache = random.randint(1, 100000)
    full_url = f"{URL}&v={nocache}"
    try:
        return pd.read_csv(full_url)
    except:
        return None

# UI
st.title("⏱️ Live PS10 - Rally Sulcis")

df = load_data()
if df is not None:
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.caption(f"Ultimo aggiornamento: {time.strftime('%H:%M:%S')}")

# Refresh ogni 25 secondi come concordato
time.sleep(25)
st.rerun()
