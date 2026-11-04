import math
import streamlit as st

st.set_page_config(
    page_title="ProBet AI - Forebet & İstatistik Merkezi",
    page_icon="⚽",
    layout="wide",
)

st.title("⚽ ProBet AI: Forebet Style & İstatistiksel Analiz Motoru")
st.markdown(
    "Küresel oranlar, Poisson olasılık matrisi ve form analizine dayalı"
    " tarafsız tahmin platformu."
)

tab1, tab2, tab3 = st.tabs(
    ["📊 Güncel Maç Bülteni", "🔍 Özel Maç Sorgulama", "🔴 Canlı Maç Takip"]
)

# Güncel ve aktif bülten maçları
FOREBET_FIXTURES = [
    {
        "lig": "Süper Lig",
        "mac": "Galatasaray vs Fenerbahçe",
        "h": "Galatasaray",
        "a": "Fenerbahçe",
        "h_form": 2.4,
        "a_form": 2.2,
    },
    {
        "lig": "Süper Lig",
        "mac": "Beşiktaş vs Trabzonspor",
        "h": "Beşiktaş",
        "a": "Trabzonspor",
        "h_form": 1.8,
        "a_form": 1.7,
    },
    {
        "lig": "Premier Lig",
        "mac": "Manchester City vs Arsenal",
        "h": "Manchester City",
        "a": "Arsenal",
        "h_form": 2.5,
        "a_form": 2.4,
    },
    {
        "lig": "Premier Lig",
        "mac": "Liverpool vs Chelsea",
        "h": "Liverpool",
        "a": "Chelsea",
        "h_form": 2.2,
        "a_form": 1.9,
    },
    {
        "lig": "La Liga",
        "mac": "Real Madrid vs Barcelona",
        "h": "Real Madrid",
        "a": "Barcelona",
        "h_form": 2.6,
        "a_form": 2.5,
    },
    {
        "lig": "Serie A",
        "mac": "Inter vs Milan",
        "h": "Inter",
        "a": "Milan",
        "h_form": 2.3,
        "a_form": 2.0,
    },
]


def poisson_prob(lmbda, k):
  return (math.exp(-lmbda) * (lmbda**k)) / math.factorial(k)


def forebet_engine(home_name, away_name, h_form_val=2.0, a_form_val=1.8):
  # Forebet tarzı Poisson ve xG hesaplaması
  h_lambda = (h_form_val * 0.55) + 0.35  # Ev sahibi avantajı
  a_lambda = a_form_val * 0.50

  max_g = 5
  best_p = 0
  best_score = (1, 1)

  hw_p, draw_p, aw_p = 0, 0, 0

  for h in range(max_g + 1):
    for a in range(max_g + 1):
      p = poisson_prob(h_lambda, h) * poisson_prob(a_lambda, a)
      if h > a:
        hw_p += p
      elif h == a:
        draw_p += p
      else:
        aw_p += p

      if p > best_p:
        best_p = p
        best_score = (h, a)

  total = hw_p + draw_p + aw_p
  p1 = round((hw_p / total) * 100, 1)
  px = round((draw_p / total) * 100, 1)
  p2 = round((aw_p / total) * 100, 1)

  o1 = round(100 / p1, 2) if p1 > 0 else 1.05
  ox = round(100 / px, 2) if px > 0 else 1.05
  o2 = round(100 / p2, 2) if p2 > 0 else 1.05

  if p1 > p2 and p1 > px:
    ms = f"MS 1 ({home_name} Favori)"
  elif p2 > p1 and p2 > px:
    ms = f"MS 2 ({away_name} Favori)"
  else:
    ms = "0 (Beraberlik Beklentisi)"

  skor_str = f"{best_score[0]} - {best_score[1]}"
  au = (
      "2.5 ÜST" if (best_score[0] + best_score[1]) > 2.2 else "2.5 ALT"
  )
  kg = (
      "KG Var" if best_score[0] > 0 and best_score[1] > 0 else "KG Yok"
  )
  guven = f"%{int(max(p1, px, p2) + 15)} (Forebet Model)"

  return p1, px, p2, o1, ox, o2, ms, skor_str, au, kg, guven


with tab1:
  st.subheader("📅 Günün Maç Bülteni (Forebet Olasılık Matrisi)")
  selected_item = st.selectbox(
      "Maç Seçin:",
      [f"{m['lig']} | {m['mac']}" for m in FOREBET_FIXTURES],
      key="fb_select",
  )

  if st.button(
      "Forebet Algoritması ile Analiz Et 🚀",
      type="primary",
      key="btn_fb_bulten",
  ):
    match_data = next(
        m
        for m in FOREBET_FIXTURES
        if f"{m['lig']} | {m['mac']}" == selected_item
    )
    p1, px, p2, o1, ox, o2, ms, skor, au, kg, guven = forebet_engine(
        match_data["h"], match_data["a"], match_data["h_form"], match_data["a_form"]
    )

    st.success(f"📊 **{match_data['mac']} — Forebet Tahmin Raporu**")

    # Oranlar ve Yüzdeler
    col_m1, col_mx, col_m2, col_g = st.columns(4)
    col_m1.metric(f"MS 1 (%{p1})", f"Oran: {o1}")
    col_mx.metric(f"MS X (%{px})", f"Oran: {ox}")
    col_m2.metric(f"MS 2 (%{p2})", f"Oran: {o2}")
    col_g.metric("Model Güveni", guven)

    st.divider()

    c1, c2, c3 = st.columns(3)
    with c1:
      st.info(f"🎯 **Forebet Maç Sonucu:**\n{ms}")
    with c2:
      st.success(f"⚽ **En Olası Skor:**\n{skor}")
    with c3:
      st.warning(f"🔥 **Alt / Üst & KG:**\n{au} | {kg}")

with tab2:
  st.subheader("🔍 Özel Maç Sorgulama (Forebet Engine)")
  sc1, sc2 = st.columns(2)
  with sc1:
    h_custom = st.text_input("Ev Sahibi Takım", value="Milan", key="fb_custom_h")
  with sc2:
    a_custom = st.text_input(
        "Deplasman Takımı", value="Roma", key="fb_custom_a"
    )

  if st.button(
      "Özel Maçı Forebet ile Analiz Et 🚀",
      type="primary",
      key="btn_fb_custom",
  ):
    p1, px, p2, o1, ox, o2, ms, skor, au, kg, guven = forebet_engine(
        h_custom, a_custom, 2.1, 1.9
    )

    st.success(f"📊 **{h_custom} vs {a_custom} — Forebet Raporu**")

    col_m1, col_mx, col_m2, col_g = st.columns(4)
    col_m1.metric(f"MS 1 (%{p1})", f"Oran: {o1}")
    col_mx.metric(f"MS X (%{px})", f"Oran: {ox}")
    col_m2.metric(f"MS 2 (%{p2})", f"Oran: {o2}")
    col_g.metric("Model Güveni", guven)

    st.divider()

    c1, c2, c3 = st.columns(3)
    with c1:
      st.info(f"🎯 **Forebet Maç Sonucu:**\n{ms}")
    with c2:
      st.success(f"⚽ **En Olası Skor:**\n{skor}")
    with c3:
      st.warning(f"🔥 **Alt / Üst & KG:**\n{au} | {kg}")

with tab3:
  st.subheader("🔴 Canlı Maç Takip Paneli")
  dakika = st.slider("Maç Dakikası", 1, 95, 70, key="fb_live_slider")
  lc1, lc2 = st.columns(2)
  with lc1:
    ev_g = st.number_input("Ev Sahibi Gol", 0, 10, 0, key="fb_live_hg")
  with lc2:
    dep_g = st.number_input("Deplasman Gol", 0, 10, 0, key="fb_live_ag")

  if st.button(
      "Canlı Forebet Sinyali Üret ⚡", type="primary", key="fb_live_btn"
  ):
    if dakika >= 75 and ev_g == dep_g:
      st.success(
          "🔥 **Forebet Canlı Sinyal:** Beraberlik skoru korunuyor! **Sıradaki"
          " Gol Var / 0.5 ÜST** değerlendirilebilir."
      )
    else:
      st.info(
          "🎯 **Forebet Canlı Sinyal:** Maç akışı istatistiksel sınırlar içinde"
          " ilerliyor."
      )
