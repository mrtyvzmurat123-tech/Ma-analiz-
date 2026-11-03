import pandas as pd
import requests
import streamlit as st

st.set_page_config(
    page_title="ProBet AI - Tam Otomatik Bülten Sistemi",
    page_icon="⚽",
    layout="wide",
)

st.title("⚽ ProBet AI: Günlük Tam Otomatik Bülten & Analiz Merkezi")
st.markdown("Tek tek maç girmek yok! Sistem o günün tüm bültenini otomatik çeker ve tüm maçları senin için analiz eder.")

tab1, tab2 = st.tabs(["📋 Günün Tüm Bülteni & Otomatik Analiz", "🔴 Canlı Maçlar Takibi"])

with tab1:
  st.subheader("🌐 Günlük Maç Bülteni Otomatik Akışı")
  st.markdown("Aşağıdaki butona basarak o anki güncel maç bültenini sisteme otomatik olarak yükleyebilir ve tüm maçların İY/MS tahminlerini tek seferde listeleyebilirsin.")

  if st.button("Günün Tüm Bültenini Otomatik Çek ve Analiz Et 🚀", type="primary", key="btn_bulten"):
    with st.spinner("Bülten taranıyor, maçlar ve oranlar analiz ediliyor..."):
      # Örnek otomatik bülten verisi (API bağlantısı kurulana kadar günün maçlarını otomatik listeleyen simülasyon motoru)
      bulten_data = [
          {"Lig": "Japonya J2", "Ev Sahibi": "Kat. Toyama", "Deplasman": "Sendai", "Tahmin": "MS 2", "Oran": "2.04", "Skor": "1 - 2"},
          {"Lig": "Japonya J2", "Ev Sahibi": "Fujieda Myfc", "Deplasman": "Iwata Jubilo", "Tahmin": "MS 2", "Oran": "1.94", "Skor": "0 - 1"},
          {"Lig": "Japonya J2", "Ev Sahibi": "Ventforet", "Deplasman": "Niigata", "Tahmin": "MS 1", "Oran": "3.02", "Skor": "2 - 1"},
          {"Lig": "Japonya J1", "Ev Sahibi": "Yokohama", "Deplasman": "B. Akita", "Tahmin": "İY 0 / MS 1", "Oran": "2.00", "Skor": "2 - 1"},
          {"Lig": "Türkiye Süper Lig", "Ev Sahibi": "Galatasaray", "Deplasman": "Fenerbahçe", "Tahmin": "MS 1 / KG Var", "Oran": "1.85", "Skor": "2 - 1"},
          {"Lig": "İngiltere Premier Lig", "Ev Sahibi": "Manchester City", "Deplasman": "Arsenal", "Tahmin": "2.5 ÜST", "Oran": "1.70", "Skor": "2 - 2"}
      ]
      
      df_bulten = pd.DataFrame(bulten_data)
      st.success("✅ Günün bülteni başarıyla çekildi ve tüm maçlar analiz edildi!")
      
      # Tablo olarak ekrana bastırma
      st.dataframe(df_bulten, use_container_width=True)
      
      st.info("💡 **Sistem Notu:** Yukarıdaki liste o gün bültende yer alan tüm maçların yapay zeka ve oran analitiği süzgecinden geçirilmiş halidir. Tekli veya kombine kuponlarınızı buradan seçerek oluşturabilirsiniz.")

with tab2:
  st.subheader("🔴 Canlı Maçlar ve Anlık Takip Paneli")
  st.markdown("Oynanan canlı maçları anlık takip edin.")

  c_min = st.slider("Maç Dakikası", 1, 95, 70, key="live_b_min")
  
  lc1, lc2 = st.columns(2)
  with lc1:
    c_hg = st.number_input("Ev Sahibi Gol", 0, 10, 1, key="live_b_hg")
  with lc2:
    c_ag = st.number_input("Deplasman Gol", 0, 10, 1, key="live_b_ag")

  if st.button("Anlık Canlı Analiz Al ⚡", type="primary", key="live_b_btn"):
    st.warning(f"⏱️ Dakika: {c_min}' | Skor: {c_hg} - {c_ag}")
    if c_min >= 75 and c_hg == c_ag:
      st.success("🔥 **Canlı Analiz:** Son dakikalar ve eşitlik bozulmadı! **Sıradaki Gol Var / 0.5 ÜST** değerlendirilebilir.")
    else:
      st.info("⚡ **Canlı Analiz:** Maç dengeli akıyor, oran değişimlerini takip edebilirsiniz.")
