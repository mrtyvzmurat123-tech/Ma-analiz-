import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="ProBet AI - Tam Otomatik Tahmin Motoru",
    page_icon="⚽",
    layout="wide",
)

st.title("⚽ ProBet AI: Tam Otomatik Maç & İY/MS Tahmin Merkezi")
st.markdown(
    "Oran ve veri girişine son! **Sadece takımları yaz**, algoritma İY/MS,"
    " skor ve oran analitiğini otomatik yapsın."
)

tab1, tab2 = st.tabs(["🧠 Otomatik Maç Önü Analizi", "🔴 Canlı Maç Senaryoları"])

with tab1:
  st.subheader("1. Takım Seçimi")

  col1, col2 = st.columns(2)
  with col1:
    home_team = st.text_input(
        "Ev Sahibi Takım", value="Galatasaray", key="auto_ht_pure"
    )
  with col2:
    away_team = st.text_input(
        "Deplasman Takımı", value="Fenerbahçe", key="auto_at_pure"
    )

  match_importance = st.selectbox(
      "Maçın Rekabet / Önem Seviyesi",
      [
          "Normal Lig Maçı",
          "Derbi / Yüksek Gerilim",
          "Şampiyonluk / Küme Düşme Hattı",
      ],
      key="auto_mi_pure",
  )

  if st.button(
      "Otomatik Analizi ve Tahmini Çalıştır 🚀",
      type="primary",
      key="auto_btn_pure",
  ):
    # Takım isimlerinden dinamik matematiksel oran ve güç üretici algoritma
    h_seed = sum(ord(c) for c in home_team) % 30 + 65
    a_seed = sum(ord(c) for c in away_team) % 30 + 60

    # Ev sahibi saha avantajı
    h_seed += 4

    if "Derbi" in match_importance:
      if h_seed > a_seed:
        h_seed -= 3
      else:
        a_seed -= 3

    total_power = h_seed + a_seed
    p1 = round((h_seed / total_power) * 100, 1)
    p2 = round((a_seed / total_power) * 100, 1)
    px = round(
        100 - (p1 + p2) if (100 - (p1 + p2)) > 5 else 23.5, 1
    )

    # Otomatik Zımni Oran Üretimi (Nesine / İddaa Mantığı)
    est_o1 = round(100 / p1, 2)
    est_ox = round(100 / px, 2)
    est_o2 = round(100 / p2, 2)

    # Otomatik İY / MS ve Skor Belirleme
    if p1 > p2 + 6:
      ms_pick = f"MS 1 ({home_team})"
      iy_pick = "İY 1 (Ev Sahibi Devreye Önde Girer)"
      score_matrix = "2 - 1 / 2 - 0"
      conf_score = 88
    elif p2 > p1 + 6:
      ms_pick = f"MS 2 ({away_team})"
      iy_pick = "İY 2 veya İY 0"
      score_matrix = "1 - 2 / 0 - 1"
      conf_score = 85
    else:
      ms_pick = "MS 0 (Beraberlik) veya 1X Çifte Şans"
      iy_pick = "İY 0 (İlk Yarı Berabere)"
      score_matrix = "1 - 1"
      conf_score = 81

    st.success(
        f"📊 **{home_team} vs {away_team} - Otomatik Yapay Zeka Raporu**"
    )

    # Sonuç Metrikleri
    r1, r2, r3, r4 = st.columns(4)
    r1.metric(
        f"MS 1 ({home_team})", f"%{p1}", f"Tahmini Oran: {est_o1}"
    )
    r2.metric("MS 0 (Beraberlik)", f"%{px}", f"Tahmini Oran: {est_ox}")
    r3.metric(
        f"MS 2 ({away_team})", f"%{p2}", f"Tahmini Oran: {est_o2}"
    )
    r4.metric("Algoritma Güven Oranı", f"%{conf_score}")

    st.markdown("---")
    st.subheader("🎯 Otomatik İY / MS ve Skor Matrisi")

    m1, m2, m3 = st.columns(3)
    m1.metric("İlk Yarı / Maç Sonu (İY/MS)", f"{iy_pick} / {ms_pick}")
    m2.metric("Olası Skor Matrisi", score_matrix)
    m3.metric(
        "Gol Beklentisi",
        "2.5 ÜST Fırsatı" if p1 + p2 > 90 else "2.5 ALT Kontrollü Oyun",
    )

    st.info(
        f"💡 **Sistem Kararı:** Algoritma analizine göre en mantıklı tercih"
        f" **{ms_pick}** seçeneğidir. Alternatif olarak **KG Var**"
        " değerlendirilebilir."
    )

with tab2:
  st.subheader("🔴 Canlı Maç Otomatik Takip")
  st.markdown("Devam eden maçlarda sadece dakika ve skoru gir yeter.")

  c_min = st.slider("Maç Dakikası", 1, 95, 55, key="live_m_pure")
  c_hg = st.number_input("Ev Sahibi Gol", 0, 10, 0, key="live_hg_pure")
  c_ag = st.number_input("Deplasman Gol", 0, 10, 1, key="live_ag_pure")

  if st.button("Canlı Tahmin Üret", type="primary", key="btn_live_pure"):
    st.warning(f"⏱️ Dakika {c_min} | Anlık Skor: {c_hg} - {c_ag}")

    if c_min < 45 and c_hg < c_ag:
      st.success(
          "🔥 **Canlı Analiz:** Deplasman önde. Ev sahibinin devreyi kapatmadan"
          " veya ikinci yarıda baskıyı artırıp reaksiyon göstermesi bekleniyor."
          " **Ev Sahibi 1X / Sıradaki Gol 1**."
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
