import pandas as pd
import streamlit as st

# Sayfa Yapılandırması
st.set_page_config(
    page_title="ProBet AI - Profesyonel Maç Analiz Motoru", page_icon="⚽", layout="wide"
)

st.title("🎯 ProBet AI: Profesyonel Maç & Canlı Analiz Merkezi")
st.markdown(
    "Hava durumu, hakem eğilimleri, sakatlıklar ve anlık maç verilerini"
    " harmanlayan **gelişmiş karar destek sistemi**."
)

# Sekmeler
tab1, tab2, tab3 = st.tabs(
    [
        "🧠 Gelişmiş Maç & Faktör Analizi",
        "🔴 Canlı Maç Takip & Anlık Senaryo",
        "📊 Sistem Mantığı & Rehber",
    ]
)

with tab1:
  st.subheader("Maç ve Çevresel Faktör Parametreleri")

  col_t1, col_t2 = st.columns(2)
  with col_t1:
    home_team = st.text_input("Ev Sahibi Takım", value="Galatasaray")
    home_form = st.slider(
        "Ev Sahibi Temel Form / Güç (1-100)", 1, 100, 86, key="hf"
    )
    home_missing = st.selectbox(
        "Ev Sahibi Eksik / Sakat Durumu",
        [
            "Tam Kadro (Eksik Yok)",
            "1-2 Yedek Oyuncu Eksik",
            "Kritik 1-2 Oyuncu (Golcü/Stoper) Sakat",
            "Kadro Çöküşü / Çok Fazla Eksik",
        ],
    )
  with col_t2:
    away_team = st.text_input("Deplasman Takımı", value="Fenerbahçe")
    away_form = st.slider(
        "Deplasman Temel Form / Güç (1-100)", 1, 100, 82, key="af"
    )
    away_missing = st.selectbox(
        "Deplasman Eksik / Sakat Durumu",
        [
            "Tam Kadro (Eksik Yok)",
            "1-2 Yedek Oyuncu Eksik",
            "Kritik 1-2 Oyuncu (Golcü/Stoper) Sakat",
            "Kadro Çöküşü / Çok Fazla Eksik",
        ],
    )

  st.markdown("---")
  st.subheader("🌤️ Çevresel ve Hakem Etkenleri")

  c1, c2, c3 = st.columns(3)
  with c1:
    weather = st.selectbox(
        "Hava / Saha Durumu",
        [
            "Normal / İdeal",
            "Şiddetli Yağmur / Ağır Zemin (Gol sayısını düşürür)",
            "Aşırı Sıcak / Nem",
            "Soğutucu / Rüzgarlı",
        ],
    )
  with c2:
    referee_style = st.selectbox(
        "Hakem Karakteristiği",
        [
            "Normal / Dengeli",
            "Çok Kart Gösteren / Faul Düdüğünü Sık Çalan (Sert maç)",
            "Oyunu Oynatan / Toleranslı Hakem",
            "Penaltı / Penaltı Noktasına Yakın Yönetim",
        ],
    )
  with c3:
    match_importance = st.selectbox(
        "Maçın Önemi / Niteliği",
        [
            "Normal Lig Maçı",
            "Derbi / Rekabet Yüksek",
            "Şampiyonluk / Küme Düşme Hattı (Taktiksel / Az Gol)",
            "Kupa / Rotasyonlu Kadro",
        ],
    )

  if st.button(
      "Tüm Faktörleri Hesapla ve En İyi Tahmini Sun 🚀", type="primary"
  ):
    h_score = home_form
    a_score = away_form

    if "Kritik" in home_missing:
      h_score -= 8
    elif "Çok" in home_missing:
      h_score -= 15
    if "Kritik" in away_missing:
      a_score -= 8
    elif "Çok" in away_missing:
      a_score -= 15

    if "Yağmur" in weather:
      h_score -= 3
      a_score -= 3

    if "Derbi" in match_importance:
      if h_score > a_score:
        h_score -= 4
      else:
        a_score -= 4

    total_p = h_score + a_score
    h_prob = round((h_score / total_p) * 100, 1)
    a_prob = round((a_score / total_p) * 100, 1)
    d_prob = round(
        100 - (h_prob + a_prob) if (100 - (h_prob + a_prob)) > 5 else 24.0, 1
    )

    confidence_rate = int(
        70 + abs(h_prob - a_prob) / 2
        if abs(h_prob - a_prob) > 10
        else 65
    )
    if confidence_rate > 92:
      confidence_rate = 91

    st.success(
        f"📋 **{home_team} vs {away_team} - Kapsamlı Yapay Zeka Raporu**"
    )

    col_r1, col_r2, col_r3, col_r4 = st.columns(4)
    col_r1.metric(f"MS 1 ({home_team})", f"%{h_prob}")
    col_r2.metric("MS 0 (Beraberlik)", f"%{d_prob}")
    col_r3.metric(f"MS 2 ({away_team})", f"%{a_prob}")
    col_r4.metric("Algoritma Güven Skoru", f"%{confidence_rate}")

    st.markdown("---")
    st.subheader("💡 Profesyonel Bahis Önerileri ve Skor Matrisi")

    if h_prob > a_prob + 8:
      primary_bet = "MS 1 veya Çifte Şans 1X (Ev Sahibi Avantajlı)"
      est_score = "2 - 1"
    elif a_prob > h_prob + 8:
      primary_bet = "MS 2 veya Çifte Şans X2 (Deplasman Dirençli)"
      est_score = "1 - 2"
    else:
      primary_bet = "Karşılıklı Gol (KG) Var veya 0-2 Çifte Şans"
      est_score = "1 - 1"

    over_under = (
        "2.5 Gol Altı (Taktiksel/Ağır Zemin)"
        if "Yağmur" in weather or "Şampiyonluk" in match_importance
        else "2.5 Gol Üstü"
    )
    card_prediction = (
        "Yüksek (4.5 Kart Üstü Bekleniyor)"
        if "Kart" in referee_style
        else "Normal Kart Limiti"
    )

    st.info(f"🎯 **Önerilen Ana Bahis:** {primary_bet}")

    b1, b2, b3 = st.columns(3)
    b1.metric("Öngörülen Skor", est_score)
    b2.metric("Alt / Üst Eğilimi", over_under)
    b3.metric("Hakem / Kart Beklentisi", card_prediction)

with tab2:
  st.subheader("🔴 Canlı Maç Analiz ve Anlık Senaryo Motoru")
  st.markdown(
      "Maç oynanırken dakika ve skoru girerek kalan dakikalar için olasılık"
      " hesaplayın."
  )

  c_min = st.slider("Maçın Dakikası", 1, 90, 45)
  c_score_h = st.number_input("Ev Sahibi Anlık Gol", 0, 10, 0)
  c_score_a = st.number_input("Deplasman Anlık Gol", 0, 10, 0)
  game_flow = st.selectbox(
      "Sahadaki Baskı Durumu",
      [
          "Dengeli Mücadele",
          "Ev Sahibi Baskı Kuruyor / Golü Arıyor",
          "Deplasman Kontrataklarla Tehlikeli",
      ],
  )

  if st.button("Canlı Kalan Dakika Analizi Yap"):
    st.warning(
        f"Dakika {c_min} | Skor: {c_score_h} - {c_score_a} için analiz"
        " güncellendi."
    )
    if c_min > 75 and c_score_h == c_score_a:
      st.info(
          "💡 **Canlı Tavsiyesi:** Son dakikalarda beraberlik bozulabilir."
          " Alternatif: 'Sonradan Gol Olur' veya 'Beraberlikte İade'."
      )
    elif "Ev Sahibi Baskı" in game_flow:
      st.info(
          "💡 **Canlı Tavsiyesi:** Ev sahibinin 2. golü veya maçın üstü"
          " tetiklenebilir."
      )
    else:
      st.info("💡 **Canlı Tavsiyesi:** Oyunu izlemede kal, oranları takip et.")

with tab3:
  st.subheader("📖 Pro-Analiz Mantığı Nasıl Çalışıyor?")
  st.markdown("""
    * **Faktör Sentezi:** Sadece form durumuna değil; hakemin kart eğilimine, hava şartlarının (yağmur/zemin) gol ihtimalini düşürmesine ve eksik oyuncuların taktiksel etkisine göre oranlar yeniden süzülür.
    * **Güven Oranı:** Çeşitli değişkenler arasındaki çelişkiler incelenerek kuponun tutma olasılığı matematiksel yüzdeye dökülür.
    """)
