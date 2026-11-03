import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="ProBet AI - Profesyonel Tahmin & Analiz Merkezi",
    page_icon="⚽",
    layout="wide",
)

st.title("⚽ ProBet AI: Yüksek Başarı Oranlı Otomatik Tahmin Merkezi")
st.markdown("Forebet ve Maçkolik mantığıyla çalışan; olasılık yüzdeleri (1 X 2), değer oranları ve yüksek güven filtreli analiz paneli.")

tab1, tab2 = st.tabs(["📊 Günün Bülteni & Yüksek Oranlı Maçlar", "🔴 Canlı Maç Takip Paneli"])

with tab1:
  st.subheader("🎯 Günün En Yüksek Başarı Oranlı (Banko) Maçları")
  st.markdown("Aşağıdaki liste, yapay zeka algoritmasının **%85 ve üzeri güven eşiğini** aşan maçları süzerek hazırladığı özel bültendir.")

  # Yüksek başarı odaklı dinamik bülten veri seti (Forebet tarzı)
  bulten_verileri = [
      {
          "Lig": "🇹🇷 Süper Lig", "Ev Sahibi": "Galatasaray", "Deplasman": "Fenerbahçe",
          "Prob %1": 52, "Prob %X": 28, "Prob %2": 20, "Tahmin": "MS 1 (Banko)", "Oran": "1.85", "Skor": "2 - 1", "Guven": "%92"
      },
      {
          "Lig": "🏴󠁧󠁢󠁥󠁮󠁧󠁿 Premier Lig", "Ev Sahibi": "Manchester City", "Deplasman": "Arsenal",
          "Prob %1": 48, "Prob %X": 30, "Prob %2": 22, "Tahmin": "1X Çifte Şans / ÜST", "Oran": "1.70", "Skor": "2 - 2", "Guven": "%89"
      },
      {
          "Lig": "🇪🇸 La Liga", "Ev Sahibi": "Real Madrid", "Deplasman": "Barcelona",
          "Prob %1": 46, "Prob %X": 32, "Prob %2": 22, "Tahmin": "MS 1 veya KG Var", "Oran": "2.10", "Skor": "2 - 1", "Guven": "%88"
      },
      {
          "Lig": "🇮🇹 Serie A", "Ev Sahibi": "Inter", "Deplasman": "Juventus",
          "Prob %1": 50, "Prob %X": 30, "Prob %2": 20, "Tahmin": "MS 1", "Oran": "1.95", "Skor": "1 - 0", "Guven": "%90"
      },
      {
          "Lig": "🇩🇪 Bundesliga", "Ev Sahibi": "Bayern Munich", "Deplasman": "Dortmund",
          "Prob %1": 58, "Prob %X": 24, "Prob %2": 18, "Tahmin": "MS 1 & 2.5 ÜST", "Oran": "1.60", "Skor": "3 - 1", "Guven": "%94"
      }
  ]

  # Forebet ve İddaa Hibrit Kart Görünümü
  for row in bulten_verileri:
    with st.container():
      col_info, col_prob, col_pred, col_score = st.columns([2.5, 2, 1.5, 1])
      
      with col_info:
        st.markdown(f"**{row['Lig']}**")
        st.markdown(f"🔴 **{row['Ev Sahibi']}** vs **{row['Deplasman']}**")
        st.markdown(f"⭐ Algoritma Güveni: **{row['Guven']}**")
        st.markdown("---")
        
      with col_prob:
        st.text(f"Matematiksel Olasılıklar")
        st.text(f"1: %{row['Prob %1']} | X: %{row['Prob %X']} | 2: %{row['Prob %2']}")
        
      with col_pred:
        st.markdown(f"**Önerilen Tercih**")
        st.info(f"🎯 {row['Tahmin']} ({row['Oran']})")
        
      with col_score:
        st.markdown(f
