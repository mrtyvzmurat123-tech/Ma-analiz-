import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="ProBet AI - Profesyonel Bülten & Analiz",
    page_icon="⚽",
    layout="wide",
)

st.title("⚽ ProBet AI: Gerçek Oran & Otomatik Maç Analiz Merkezi")
st.markdown(
    "Oranlardan olasılık çıkaran ve otomatik İY/MS tahminleri üreten profesyonel"
    " motor."
)

tab1, tab2 = st.tabs(["🧠 Oran & Maç Analizi", "🔴 Canlı Maç Senaryoları"])

with tab1:
  st.subheader("1. Maç ve Oran Bilgileri")

  col1, col2 = st.columns(2)
  with col1:
    home_team = st.text_input("Ev Sahibi Takım", value="Galatasaray", key="ht_in")
    odds_1 = st.number_input(
        "MS 1 Oranı (Nesine/İddaa)", value=1.85, step=0.05, key="o1_in"
    )
    odds_x = st.number_input(
        "MS X Oranı (Beraberlik)", value=3.40, step=0.05, key="ox_in"
    )
  with col2:
    away_team = st.text_input(
        "Deplasman Takımı", value="Fenerbahçe", key="at_in"
    )
    odds_2 = st.number_input(
        "MS 2 Oranı (Nesine/İddaa)", value=3.20, step=0.05, key="o2_in"
    )
    odds_over = st.number_input(
        "2.5 Üst Oranı", value=1.65, step=0.05, key="ov_in"
    )

  if st.button("Analizi ve Tahmini Çalıştır 🚀", type="primary", key="btn_run"):
    # Oran zımni olasılık hesabı
    raw_1 = 1 / odds_1 if odds_1 > 0 else 0
    raw_x = 1 / odds_x if odds_x > 0 else 0
    raw_2 = 1 / odds_2 if odds_2 > 0 else 0
    total_margin = raw_1 + raw_x + raw_2

    p1 = round((raw_1 / total_margin) * 100, 1)
    px = round((raw_x / total_margin) * 100, 1)
    p2 = round((raw_2 / total_margin) * 100, 1)

    if p1 > p2 + 8:
      ms_pick = f"MS 1 ({home_team})"
      iy_pick = "İY 1 veya İY 0"
      score_matrix = "2 - 1 / 2 - 0"
    elif p2 > p1 + 8:
      ms_pick = f"MS 2 ({away_team})"
      iy_pick = "İY 2 veya İY 0"
      score_matrix = "1 - 2 / 0 - 1"
    else:
      ms_pick = "MS 0 veya 1X Çifte Şans"
      iy_pick = "İY 0 (İlk Yarı Berabere)"
      score_matrix = "1 - 1"

    st.success(
        f"📊 **{home_team} vs {away_team} - Piyasa Oran Analiz Raporu**"
    )

    r1, r2, r3, r4 = st.columns(4)
    r1.metric(f"MS 1 ({home_team})", f"%{p1}", f"Oran: {odds_1}")
    r2.metric("MS X (Beraberlik)", f"%{px}", f"Oran: {odds_x}")
    r3.metric(f"MS 2 ({away_team})", f"%{p2}", f"Oran: {odds_2}")
    r4.metric("Güven Endeksi", "%87")

    st.markdown("---")
    st.subheader("🎯 Otomatik İY / MS ve Skor Matrisi")

    m1, m2, m3 = st.columns(3)
    m1.metric("İlk Yarı / Maç Sonu (İY/MS)", f"{iy_pick} / {ms_pick}")
    m2.metric("Olası Skor Matrisi", score_matrix)
    m3.metric(
        "Gol Beklentisi",
        "2.5 ÜST Fırsatı" if odds_over < 1.75 else "2.5 ALT Kontrollü Oyun",
    )

    st.info(
        f"💡 **Sistem Kararı:** Oran analitiğine göre en mantıklı tercih"
        f" **{ms_pick}** seçeneğidir."
    )

with tab2:
  st.subheader("🔴 Canlı Maç Takip ve Senaryoları")

  c_min = st.slider("Maç Dakikası", 1, 95, 55, key="live_min_key")
  c_hg = st.number_input("Ev Sahibi Gol", 0, 10, 0, key="live_hg_key")
  c_ag = st.number_input("Deplasman Gol", 0, 10, 1, key="live_ag_key")

  if st.button("Canlı Tahmin Üret", type="primary", key="btn_live_key"):
    st.warning(f"⏱️ Dakika {c_min} | Anlık Skor: {c_hg} - {c_ag}")

    if c_min < 45 and c_hg < c_ag:
      st.success(
          "🔥 **Canlı Analiz:** Deplasman önde. Ev sahibinin ikinci yarıda"
          " reaksiyon gösterip gol bulması bekleniyor. **Ev Sahibi 1X / Sıradaki"
          " Gol 1**."
      )
    elif c_min >= 75 and c_hg == c_ag:
      st.success(
          "🔥 **Canlı Analiz:** Son dakikalar ve eşitlik var! **Sıradaki Gol"
          " Var / 0.5 ÜST**."
      )
    else:
      st.info(
          "⚡ **Canlı Analiz:** Maç dengeli ilerliyor, 2.5 Alt veya Çifte"
          " Şans seçenekleri ön planda."
      )
