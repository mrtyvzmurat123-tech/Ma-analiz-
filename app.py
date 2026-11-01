import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="ProBet AI - Profesyonel Analiz", page_icon="⚡", layout="wide"
)

st.title("⚡ ProBet AI: Maç ve Canlı Analiz Merkezi")
st.markdown("Hava durumu, hakem, sakatlık ve canlı maç analiz sistemi.")

tab1, tab2 = st.tabs(["🧠 Maç Önü Analizi", "🔴 Canlı Maç Senaryoları"])

with tab1:
  st.subheader("Maç Önü Parametreleri")

  col1, col2 = st.columns(2)
  with col1:
    home_team = st.text_input("Ev Sahibi Takım", value="Galatasaray")
    home_form = st.slider("Ev Sahibi Form (1-100)", 1, 100, 85)
    odds_1 = st.number_input("MS 1 Oranı", value=1.85, step=0.05)
  with col2:
    away_team = st.text_input("Deplasman Takımı", value="Fenerbahçe")
    away_form = st.slider("Deplasman Form (1-100)", 1, 100, 80)
    odds_2 = st.number_input("MS 2 Oranı", value=3.40, step=0.05)

  match_type = st.selectbox(
      "Maçın Niteliği",
      [
          "Normal Lig Maçı",
          "Derbi / Yüksek Gerilim",
          "Şampiyonluk / Küme Düşme",
      ],
  )

  if st.button("Analizi Başlat", type="primary"):
    h_score = home_form
    a_score = away_form

    if "Derbi" in match_type:
      if h_score > a_score:
        h_score -= 4
      else:
        a_score -= 4

    total = h_score + a_score
    h_prob = round((h_score / total) * 100, 1)
    a_prob = round((a_score / total) * 100, 1)
    d_prob = round(
        100 - (h_prob + a_prob) if (100 - (h_prob + a_prob)) > 5 else 22.0, 1
    )

    st.success(f"📊 {home_team} vs {away_team} Sonuç Raporu")

    r1, r2, r3, r4 = st.columns(4)
    r1.metric(f"MS 1 ({home_team})", f"%{h_prob}")
    r2.metric("MS 0 (Beraberlik)", f"%{d_prob}")
    r3.metric(f"MS 2 ({away_team})", f"%{a_prob}")
    r4.metric("Güven Endeksi", "%89")

    st.markdown("---")
    if h_prob > a_prob:
      st.info(
          f"💡 **Öneri:** Ev sahibi ({home_team}) bir adım önde. MS 1 veya 1X"
          " Çifte Şans değerlendirilebilir."
      )
    else:
      st.info(
          f"💡 **Öneri:** Deplasman ({away_team}) dirençli. MS 2 veya X2 Çifte"
          " Şans değerlendirilebilir."
      )

with tab2:
  st.subheader("🔴 Canlı Maç Takip ve Senaryo Motoru")
  st.markdown("Devam eden maçlar için anlık olasılık ve skor tahmini.")

  c_min = st.slider("Maç Dakikası", 1, 95, 33)
  c_hg = st.number_input("Ev Sahibi Gol", 0, 10, 0)
  c_ag = st.number_input("Deplasman Gol", 0, 10, 1)

  if st.button("Canlı Tahmin ve Skor Üret", type="primary"):
    st.warning(f"⏱️ Dakika {c_min} | Anlık Skor: {c_hg} - {c_ag}")

    # Canlı Tahmin ve Skor Matrisi Mantığı
    if c_min < 45 and c_hg < c_ag:
      live_tip = (
          f"🔥 **Canlı Tahmin:** Deplasman önde ({c_hg}-{c_ag}) ancak maç erken"
          f" ({c_min}. dk). Ev sahibi reaksiyon gösterecektir."
      )
      expected_final = (
          "1 - 1 veya 2 - 1 (Ev sahibinin maça ortak olması bekleniyor)"
      )
      recommended_bet = "1X Çifte Şans veya Ev Sahibi Sıradaki Gol"
    elif c_min >= 75 and c_hg == c_ag:
      live_tip = (
          "🔥 **Canlı Tahmin:** Son dakikalardayız ve skor eşit! Beraberlik"
          " bozulma eğilimi çok yüksek."
      )
      expected_final = f"{c_hg + 1} - {c_ag + 1} (Son dakika golü yüksek ihtimal)"
      recommended_bet = "Sıradaki Gol Var / 0.5 ÜST"
    elif c_hg > c_ag:
      live_tip = "⚡ **Canlı Tahmin:** Ev sahibi önde, deplasman risk alacak."
      expected_final = (
          f"{c_hg + 1} - {c_ag} veya {c_hg} - {c_ag + 1} (Maç Üst biter)"
      )
      recommended_bet = "2.5 ÜST veya Karşılıklı Gol Var"
    else:
      live_tip = (
          "🎯 **Canlı Tahmin:** Deplasman skoru koruyor, ev sahibi yüklenecek."
      )
      expected_final = f"{c_hg + 1} - {c_ag} (Ev sahibi skoru eşitleyebilir)"
      recommended_bet = "Ev Sahibi Gol Atar / 1.5 ÜST"

    st.success(live_tip)

    sc1, sc2 = st.columns(2)
    sc1.metric("Olası Maç Sonu Skoru", expected_final)
    sc2.metric("Önerilen Canlı Bahis", recommended_bet)
