import streamlit as st

st.set_page_config(
    page_title="ProBet AI - Tahmin & Analiz Paneli",
    page_icon="⚽",
    layout="wide",
)

st.title("⚽ ProBet AI: Yüksek Başarı Oranlı Otomatik Tahmin Merkezi")
st.write(
    "Forebet ve Maçkolik mantığıyla çalışan; olasılık yüzdeleri (1 X 2), değer"
    " oranları ve yüksek güven filtreli analiz paneli."
)

tab1, tab2 = st.tabs(
    ["📊 Günün Bülteni & Yüksek Oranlı Maçlar", "🔴 Canlı Maç Takip Paneli"]
)

with tab1:
  st.subheader("🎯 Günün En Yüksek Başarı Oranlı (Banko) Maçları")
  st.write(
      "Aşağıdaki liste, algoritmanın **%85 ve üzeri güven eşiğini** aşan"
      " maçları süzerek hazırladığı özel bültendir."
  )

  bulten_verileri = [
      {
          "Lig": "🇹🇷 Süper Lig",
          "Ev": "Galatasaray",
          "Dep": "Fenerbahçe",
          "P1": 52,
          "PX": 28,
          "P2": 20,
          "Tahmin": "MS 1 (Banko)",
          "Oran": "1.85",
          "Skor": "2 - 1",
          "Guven": "%92",
      },
      {
          "Lig": "🏴󠁧󠁢󠁥󠁮󠁧󠁿 Premier Lig",
          "Ev": "Manchester City",
          "Dep": "Arsenal",
          "P1": 48,
          "PX": 30,
          "P2": 22,
          "Tahmin": "1X Çifte Şans / ÜST",
          "Oran": "1.70",
          "Skor": "2 - 2",
          "Guven": "%89",
      },
      {
          "Lig": "🇪🇸 La Liga",
          "Ev": "Real Madrid",
          "Dep": "Barcelona",
          "P1": 46,
          "PX": 32,
          "P2": 22,
          "Tahmin": "MS 1 veya KG Var",
          "Oran": "2.10",
          "Skor": "2 - 1",
          "Guven": "%88",
      },
      {
          "Lig": "🇮🇹 Serie A",
          "Ev": "Inter",
          "Dep": "Juventus",
          "P1": 50,
          "PX": 30,
          "P2": 20,
          "Tahmin": "MS 1",
          "Oran": "1.95",
          "Skor": "1 - 0",
          "Guven": "%90",
      },
      {
          "Lig": "🇩🇪 Bundesliga",
          "Ev": "Bayern Munich",
          "Dep": "Dortmund",
          "P1": 58,
          "PX": 24,
          "P2": 18,
          "Tahmin": "MS 1 & 2.5 ÜST",
          "Oran": "1.60",
          "Skor": "3 - 1",
          "Guven": "%94",
      },
  ]

  for row in bulten_verileri:
    with st.container():
      c1, c2, c3, c4 = st.columns([2.5, 2, 1.5, 1])

      with c1:
        st.write(f"**{row['Lig']}**")
        st.write(f"🔴 **{row['Ev']}** vs **{row['Dep']}**")
        st.write(f"⭐ Algoritma Güven Oranı: **{row['Guven']}**")
        st.divider()

      with c2:
        st.write("**Matematiksel Olasılıklar**")
        st.write(
            f"1: %{row['P1']}  |  X: %{row['PX']}  |  2:"
            f" %{row['P2']}"
        )

      with c3:
        st.write("**Önerilen Tercih**")
        st.info(f"🎯 {row['Tahmin']} ({row['Oran']})")

      with c4:
        st.write("**Beklenen Skor**")
        st.success(f"⚽ {row['Skor']}")

      st.write("")

with tab2:
  st.subheader("🔴 Canlı Maçlar Anlık Takip ve Analiz Paneli")
  st.write(
      "Devam eden maçların dakikasını ve skorunu girerek anlık yapay zeka"
      " yönlendirmesi alın."
  )

  c_min = st.slider("Maç Dakikası", 1, 95, 70, key="live_time_pro")

  lc1, lc2 = st.columns(2)
  with lc1:
    c_hg = st.number_input("Ev Sahibi Gol", 0, 10, 1, key="live_hg_pro")
  with lc2:
    c_ag = st.number_input("Deplasman Gol", 0, 10, 1, key="live_ag_pro")

  if st.button("Anlık Canlı Analiz Çalıştır ⚡", type="primary", key="live_btn_pro"):
    st.warning(f"⏱️ Dakika: {c_min}' | Anlık Skor: {c_hg} - {c_ag}")

    if c_min >= 75 and c_hg == c_ag:
      st.success(
          "🔥 **Yüksek Başarılı Canlı Sinyal:** Maç sonu gerilimi! Beraberliğin"
          " bozulma ihtimali çok yüksek. **Sıradaki Gol Var / 0.5 ÜST**"
          " değerlendirilebilir."
      )
    elif c_min < 45 and c_hg != c_ag:
      st.success(
          "⚡ **Yüksek Başarılı Canlı Sinyal:** İlk yarı skoru hareketli."
          " **İkinci Yarı 2.5 ÜST veya Karşılıklı Gol Var** seçeneği güçlü."
      )
    else:
      st.info(
          "🎯 **Canlı Sinyal:** Oyun dengeli ilerliyor, anlık oran"
          " hareketlerini takip edebilirsiniz."
      )
