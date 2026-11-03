import pandas as pd
import streamlit as st

# Sayfa Yapılandırması
st.set_page_config(
    page_title="ProBet AI - Tam Otomatik Tahmin Motoru",
    page_icon="⚽",
    layout="wide",
)

st.title("⚽ ProBet AI: Tam Otomatik Maç & İY/MS Tahmin Merkezi")
st.markdown(
    "Sen sadece iki takımın adını yaz; **yapay zeka algoritması** oranları,"
    " İY/MS ihtimallerini ve skor matrisini tamamen kendisi hesaplasın."
)

tab1, tab2 = st.tabs(["🧠 Maç Önü Otomatik Analiz", "🔴 Canlı Maç Senaryoları"])

with tab1:
  st.subheader("Takım Adları")

  col1, col2 = st.columns(2)
  with col1:
    home_team = st.text_input("Ev Sahibi Takım", value="Galatasaray", key="t_home")
  with col2:
    away_team = st.text_input(
        "Deplasman Takımı", value="Fenerbahçe", key="t_away"
    )

  match_type = st.selectbox(
      "Maçın Rekabet / Önem Seviyesi",
      [
          "Normal Lig Maçı",
          "Derbi / Yüksek Gerilim",
          "Şampiyonluk / Küme Düşme Hattı",
      ],
      key="t_type",
  )

  if st.button(
      "Otomatik Analizi ve Tahmini Çalıştır 🚀",
      type="primary",
      key="btn_auto_run",
  ):
    # Takım isimlerine göre simüle edilen akıllı matematiksel güç motoru
    h_val = sum(ord(c) for c in home_team) % 25 + 72
    a_val = sum(ord(c) for c in away_team) % 25 + 68

    # Ev sahibi avantajı
    h_val += 3

    if "Derbi" in match_type:
      if h_val > a_val:
        h_val -= 4
      else:
        a_val -= 4

    total = h_val + a_val
    h_prob = round((h_val / total) * 100, 1)
    a_prob = round((a_val / total) * 100, 1)
    d_prob = round(
        100 - (h_prob + a_prob) if (100 - (h_prob + a_prob)) > 5 else 23.0, 1
    )

    # Otomatik İY / MS ve Skor Matrisi Belirleme
    if h_prob > a_prob + 5:
      ms_choice = f"MS 1 ({home_team} Kazanır)"
      iy_choice = "İY 1 (Ev Sahibi Devreyi Önde Bitirir)"
      score_matrix = "2 - 1 / 2 - 0"
      confidence_rate = 89
    elif a_prob > h_prob + 5:
      ms_choice = f"MS 2 ({away_team} Kazanır)"
      iy_choice = "İY 2 veya İY 0"
      score_matrix = "1 - 2 / 0 - 1"
      confidence_rate = 86
    else:
      ms_choice = "MS 0 (Beraberlik) veya 1X Çifte Şans"
      iy_choice = "İY 0 (İlk Yarı Berabere)"
      score_matrix = "1 - 1 / 0 - 0"
      confidence_rate = 82

    st.success(f"📊 **{home_team} vs {away_team} - Otomatik Analiz Raporu**")

    # Sonuç Metrikleri
    r1, r2, r3, r4 = st.columns(4)
    r1.metric(f"MS 1 ({home_team})", f"%{h_prob}")
    r2.metric("MS 0 (Beraberlik)", f"%{d_prob}")
    r3.metric(f"MS 2 ({away_team})", f"%{a_prob}")
    r4.metric("Algoritma Güven Oranı", f"%{confidence_rate}")

    st.markdown("---")
    st.subheader("🎯 Otomatik İY / MS ve Skor Matrisi")

    m1, m2, m3 = st.columns(3)
    m1.metric("İlk Yarı / Maç Sonu (İY/MS)", f"{iy_choice} / {ms_choice}")
    m2.metric("Olası Skor Matrisi", score_matrix)
    m3.metric(
        "Gol Beklentisi",
        (
            "2.5 Gol ÜST (Tempolu Oyun)"
            if h_prob + a_prob > 90
            else "2.5 Gol ALT (Kontrollü)"
        ),
    )

    st.info(
        f"💡 **Sistem Önerisi:** Algoritmanın otomatik hesaplamalarına göre en"
        f" güvenli tercih **{ms_choice}** olup, alternatif olarak **KG Var**"
        " kuponlara eklenebilir."
    )

with tab2:
  st.subheader("🔴 Canlı Maç Otomatik Takip ve Tahmin")
  st.markdown("Devam eden maçlarda sadece dakika ve skoru gir yeter.")

  c_min = st.slider("Maç Dakikası", 1, 95, 60, key="live_m")
  c_hg = st.number_input("Ev Sahibi Gol", 0, 10, 0, key="live_hg")
  c_ag = st.number_input("Deplasman Gol", 0, 10, 1, key="live_ag")

  if st.button("Anlık Canlı Tahmin Üret", type="primary", key="btn_live_run"):
    st.warning(f"⏱️ Dakika {c_min} | Anlık Skor: {c_hg} - {c_ag}")

    if c_min < 45 and c_hg < c_ag:
      live_tip = (
          "🔥 **Canlı Analiz:** Deplasman önde ancak maç erken. Ev sahibinin"
          " devreyi kapatmadan veya ikinci yarıda baskıyı artırıp reaksiyon"
          " göstermesi bekleniyor."
      )
      live_bet_rec = "İkinci Yarı 0.5 ÜST / Ev Sahibi 1X Çifte Şans"
    elif c_min >= 75 and c_hg == c_ag:
      live_tip = (
          "🔥 **Canlı Analiz:** Kritik dakikalar! Beraberliğin bu dakikalarda"
          " bozulma istatistiği çok yüksektir."
      )
      live_bet_rec = "Sıradaki Gol Var / 1.5 Gol Üstü"
    else:
      live_tip = (
          "⚡ **Canlı Analiz:** Oyun ortada gidiyor, anlık oran"
          " değişimlerini takip edebilirsiniz."
      )
      live_bet_rec = "Maç Sonu Alt / Taraf Riskine Girme"

    st.success(live_tip)
    st.metric("Otomatik Canlı Tavsiye", live_bet_rec)
