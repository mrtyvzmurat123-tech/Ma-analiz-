import numpy as np
import pandas as pd
import requests
import streamlit as st

st.set_page_config(
    page_title="ProBet AI - Gerçek Bülten Entegrasyonu",
    page_icon="⚽",
    layout="wide",
)

st.title("⚽ ProBet AI: Gerçek Veri & Bülten Analiz Terminali")
st.markdown(
    "Nesine / Maçkolik oran mantığı ve **gerçek futbol veri servisleri**"
    " entegre edilmiş analiz motoru."
)

tab1, tab2, tab3 = st.tabs(
    [
        "📊 Günlük Bülten & Maç Analizi",
        "📂 Bülten Dosyası (Excel/CSV) Yükle",
        "🌐 Canlı API Ayarları",
    ]
)

with tab1:
  st.subheader("1. Güncel Maç ve Oran Verileri")
  st.markdown(
      "Nesine / Maçkolik bültenindeki gerçek oranları ve maç bilgilerini girin."
  )

  col1, col2 = st.columns(2)
  with col1:
    home_team = st.text_input("Ev Sahibi Takım", value="Galatasaray", key="r_ht")
    odds_1 = st.number_input(
        "MS 1 Oranı (Nesine / İddaa)", value=1.85, step=0.01, key="r_o1"
    )
    odds_x = st.number_input(
        "MS X (Beraberlik) Oranı", value=3.40, step=0.01, key="r_ox"
    )
  with col2:
    away_team = st.text_input(
        "Deplasman Takımı", value="Fenerbahçe", key="r_at"
    )
    odds_2 = st.number_input(
        "MS 2 Oranı (Nesine / İddaa)", value=3.20, step=0.01, key="r_o2"
    )
    odds_over = st.number_input(
        "2.5 Üst Oranı", value=1.65, step=0.01, key="r_oover"
    )

  if st.button(
      "Gerçek Oran Algoritmasını Çalıştır 🚀", type
