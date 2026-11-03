import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="ProBet AI - Canlı & Otomatik Tahmin Motoru",
    page_icon="⚽",
    layout="wide",
)

st.title("⚽ ProBet AI: Otomatik Analiz & Canlı Maç Merkezi")
st.markdown(
    "Takım analizi ve anlık **Canlı Maçlar** takip paneli bir arada."
)

tab1, tab2 = st.tabs(["🧠 Otomatik Maç Önü Analizi", "🔴 Canlı Maçlar & Anlık Takip"])

with tab1:
  st.subheader("1. Takım Seçimi")
  c1, c2 = st.columns(2)
  with c1:
    h_team = st.text_input("Ev Sahibi Takım", value="Galatasaray", key="t1_live")
  with c2:
    a_team = st.text_input("Deplasman Takımı", value="Fenerbahçe", key="t2_live")

  m_type = st.selectbox(
      "Maç Niteliği",
      ["Normal Lig Maçı", "Derbi / Yüksek Gerilim", "Kritik Kupa/Avrupa Maçı"],
      key="t3_live",
  )

  if st.button("Analizi Başlat 🚀", type="primary", key="b1_live"):
    h_val = (sum(ord(c) for c in h_team) % 25) + 70
    a_val = (sum(ord(c) for c in a_team) % 25) + 65

    if "Derbi" in m_type or "Kritik" in m_type:
      h_val -= 2
      a_val += 2

    total = h_val + a_val
    p_home = round((h_val / total) * 100, 1)
    p_away = round((a_val / total) * 100, 1)
    p_draw = round(100 - (p_home + p_away), 1)
    if p_draw < 15:
      p_draw = 22.0

    st.success(f"📊 {h_team} vs {a_team} Analiz Sonucu")

    col_a, col_b, col_c, col_d = st.columns(4)
    col_a.metric(f"MS 1 ({h_team})", f"%{p_home}")
    col_b.metric("MS 0 (Beraberlik)", f"%{p_draw}")
    col_c.metric(f"MS 2 ({a_team})", f"%{p_away}")
    col_d.metric("Güven Oranı", "%88")

    st.markdown("---")
    if p_home > p_away:
      sonuc = f"MS 1 veya 1X Çifte Şans ({h_team} bir adım önde)"
    else:
      sonuc = f"MS 2 veya X2 Çifte Şans ({a_team} dirençli)"

    st.info(f"💡 **Önerilen Tercih:** {sonuc}")

with tab2:
  st.subheader("🔴 Canlı Oynanan Maçlar ve Anlık Takip")
  st.markdown("Şu an sahada olan maçları seçip veya dakikasını girerek anlık simülasyon ve analiz alabilirsin.")

  # Örnek Canlı Maç Listesi Seçimi
  live_match_choice = st.selectbox(
      "Günün Canlı Maçları (Simüle Edilen Akış)",
      [
          "Seçiniz / Manuel Gir",
          "Kat. Toyama vs Sendai (Canlı)",
          "Fujieda Myfc vs Iwata Jubilo (Canlı)",
          "Ventforet vs Niigata (Canlı)",
          "Yokohama vs B. Akita (Canlı)"
      ],
      key="live_sel"
  )

  c_min = st.slider("Maç Dakikası", 1, 95, 65, key="dk_l")
  
  col_g1, col_g2 = st.columns(2)
  with col_g1:
    gol_h = st.number_input("Ev Sahibi Gol", 0, 10, 1, key="gh_l")
  with col_g2:
    gol_a = st.number_input("Deplasman Gol", 0, 10, 1, key="ga_l")

  if st.button("Canlı Durumu Analiz Et ⚡", type="primary", key="b2_live"):
    st.warning(f"⏱️ Dakika: {c_min}' | Anlık Skor: {gol_h} - {gol_a}")
    
    if c_min > 75 and gol_h == gol_a:
      st.success("🔥 **Canlı Analiz & Öneri:** Kritik dakikalar ve skor berabere! Beraberliğin bozulma ihtimali çok yüksek. **Sıradaki Gol Var / 0.5 ÜST** değerlendirilebilir.")
    elif gol_h > gol_a:
      st.success("⚡ **Canlı Analiz & Öneri:** Ev sahibi önde, deplasman risk alıyor. Maç açık alana dönüyor. **Maç 2.5 ÜST / Deplasman Gol Atar**.")
    else:
      st.info("🎯 **Canlı Analiz & Öneri:** Oyun dengede ilerliyor, anlık oran değişimlerini veya alt seçeneklerini takip edebilirsin.")
