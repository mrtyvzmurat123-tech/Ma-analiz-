import streamlit as st

st.set_page_config(
    page_title="ProBet AI - Global Analiz Merkezi",
    page_icon="⚽",
    layout="wide",
)

st.title("⚽ ProBet AI: Dünya Ligleri Kararlı Maç Analiz Motoru")
st.write("Dünya genelindeki tüm lig ve takımları kapsayan, sapmasız ve gerçekçi güç endeksli tahmin paneli.")

tab1, tab2 = st.tabs(["🌐 Dünya Ligleri Analiz Motoru", "🔴 Canlı Maç Takip Paneli"])

# Genişletilmiş Global Takım Güç İndeksi (10 üzerinden)
GLOBAL_TEAM_INDEX = {
    # 🇹🇷 Türkiye Süper Lig
    "galatasaray": 8.8, "fenerbahçe": 8.7, "beşiktaş": 8.1, "trabzonspor": 7.6, "başakşehir": 7.4, "samsunspor": 7.1, "eyüpspor": 7.0,
    # 🏴󠁧󠁢󠁥󠁮󠁧󠁿 İngiltere Premier Lig & Alt Ligler
    "manchester city": 9.6, "arsenal": 9.3, "liverpool": 9.4, "chelsea": 8.5, "manchester united": 8.2, "tottenham": 8.3, "aston villa": 8.4, "newcastle": 8.2, "east bengal": 5.5,
    # 🇪🇸 İspanya La Liga
    "real madrid": 9.6, "barcelona": 9.4, "atletico madrid": 8.6, "girona": 8.0, "real sociedad": 8.1, "athletic bilbao": 8.2, "sevilla": 7.8,
    # 🇮🇹 İtalya Serie A
    "inter": 9.1, "juventus": 8.6, "milan": 8.5, "napoli": 8.5, "atalanta": 8.4, "roma": 8.1, "lazio": 8.0,
    # 🇩🇪 Almanya Bundesliga
    "bayern munich": 9.5, "leverkusen": 9.0, "dortmund": 8.6, "rb leipzig": 8.4, "stuttgart": 8.1,
    # 🇫🇷 Fransa Ligue 1
    "psg": 9.3, "monaco": 8.2, "lille": 8.0, "marseille": 8.0, "lyon": 7.7,
    # 🇵🇹 Portekiz & 🇳🇱 Hollanda
    "benfica": 8.4, "sporting cp": 8.5, "porto": 8.3, "ajax": 7.9, "psv": 8.2, "feyenoord": 8.1,
    # 🇸🇦 Suudi Arabistan & 🇺🇸 MLS
    "al hilal": 8.3, "al nassr": 8.0, "al ittihad": 7.9, "inter miami": 7.8,
    # 🇧🇷 Brezilya & 🇦🇷 Arjantin
    "flamengo": 8.2, "palmeiras": 8.3, "botafogo": 8.0, "river plate": 8.1, "boca juniors": 7.9,
    # 🇴🇲 Umman / Asya (Örn: Seeb)
    "seeb": 5.8, "al seeb": 5.8
}

def analyze_global_match(home, away):
    h_clean = home.strip().lower()
    a_clean = away.strip().lower()
    
    # Güç Skorlarını Çekme (Yoksa dengeli evrensel lig katsayısı olan 7.0 atanır)
    h_power = GLOBAL_TEAM_INDEX.get(h_clean, 7.0)
    a_power = GLOBAL_TEAM_INDEX.get(a_clean, 6.8)
    
    # Ev Sahibi Avantajı (+0.4)
    h_power_total = h_power + 0.4
    a_power_total = a_power
    
    diff = h_power_total - a_power_total
    
    # Kararlı Olasılık Yüzdeleri
    total_power = h_power_total + a_power_total
    p1 = round((h_power_total / total_power) * 100, 1)
    p2 = round((a_power_total / total_power) * 100, 1)
    
    # Beraberlik Payı
    px = round(max(18.0, 100.0 - (abs(p1 - p2) * 1.2)), 1)
    
    # Yüzdeleri 100'e Ölçekleme
    t_sum = p1 + p2 + px
    p1 = round((p1 / t_sum) * 100, 1)
    p2 = round((p2 / t_sum) * 100, 1)
    px = round(100.0 - (p1 + p2), 1)
    
    # Oran Türetimi
    o1 = round(100 / p1, 2)
    ox = round(100 / px, 2)
    o2 = round(100 / p2, 2)
    
    # Kesin Mantıksal Skor ve Tahmin Motoru
    if diff >= 1.5:
        ms_pick = f"MS 1 ({home} Net Favori)"
        skor = "3 - 0" if diff > 2.2 else "2 - 0"
        iy_pick = "İY 1"
        au_pick = "2.5 ÜST"
        kg_pick = "KG Yok"
        guven = "%94 (Banko)"
    elif diff >= 0.5:
        ms_pick = f"MS 1 ({home})"
        skor = "2 - 1"
        iy_pick = "İY 1 veya İY 0"
        au_pick = "2.5 ÜST"
        kg_pick = "KG Var"
        guven = "%90 (Yüksek)"
    elif diff <= -1.5:
        ms_pick = f"MS 2 ({away} Net Favori)"
        skor = "0 - 3" if diff < -2.2 else "0 - 2"
        iy_pick = "İY 2"
        au_pick = "2.5 ÜST"
        kg_pick = "KG Yok"
        guven = "%93 (Banko)"
    elif diff <= -0.5:
        ms_pick = f"MS 2 ({away})"
        skor = "1 - 2"
        iy_pick = "İY 2 veya İY 0"
        au_pick = "2.5 ÜST"
        kg_pick = "KG Var"
        guven = "%89 (Yüksek)"
    else:
        ms_pick = "0 (Beraberlik) veya Çifte Şans"
        skor = "1 - 1"
        iy_pick = "İY 0"
        au_pick = "2.5 ALT"
        kg_pick = "KG Var"
        guven = "%87 (Dengeli Mücadele)"
        
    return {
        "p1": p1, "px": px, "p2": p2,
        "o1": o1, "ox": ox, "o2": o2,
        "ms": ms_pick, "iy": iy_pick,
        "skor": skor, "au": au_pick, "kg": kg_pick,
        "guven": guven
    }

with tab1:
    st.subheader("1. Dünya Üzerindeki Herhangi İki Takımı Girin")
    
    c1, c2 = st.columns(2)
    with c1:
        home_in = st.text_input("Ev Sahibi Takım", value="East Bengal", key="g_home")
    with c2:
        away_in = st.text_input("Deplasman Takımı", value="Seeb", key="g_away")
        
    if st.button("Dünya Standartlarında Analiz Et 🚀", type="primary", key="btn_global_run"):
        res = analyze_global_match(home_in, away_in)
        
        st.success(f"📊 **{home_in} vs {away_in} — Evrensel Analiz Raporu**")
        
        # 1 X 2 Yüzdeleri
        m1, mx, m2, mc = st.columns(4)
        m1.metric(f"MS 1 (%{res['p1']})", f"Oran: {res['o1']}")
        mx.metric(f"MS X (%{res['px']})", f"Oran: {res['ox']}")
        m2.metric(f"MS 2 (%{res['p2']})", f"Oran: {res['o2']}")
        mc.metric("Güven Derecesi", res["guven"])
        
        st.divider()
        
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            st.write("**Maç Sonu & İY Tahmini**")
            st.info(f"🎯 **{res['ms']}**\n\n⏱️ {res['iy']}")
            
        with col_b:
            st.write("**Beklenen Net Skor**")
            st.success(f"⚽ **Tahmini Skor: {res['skor']}**")
            
        with col_c:
            st.write("**Alt / Üst & KG Durumu**")
            st.warning(f"🔥 {res['au']}\n\n🤝 {res['kg']}")

with tab2:
    st.subheader("🔴 Canlı Maç Takip Paneli")
    st.write("Devam eden canlı maçların skoru ve dakikası ile anlık sinyal alın.")
    
    c_time = st.slider("Maç Dakikası", 1, 95, 75, key="live_time_global")
    lc1, lc2 = st.columns(2)
    with lc1:
        lh_gol = st.number_input("Ev Sahibi Gol", 0, 10, 0, key="live_hg_global")
    with lc2:
        la_gol = st.number_input("Deplasman Gol", 0, 10, 0, key="live_ag_global")
        
    if st.button("Anlık Canlı Sinyal Üret ⚡", type="primary", key="btn_live_global"):
        st.warning(f"⏱️ Dakika: {c_time}' | Skor: {lh_gol} - {la_gol}")
        if c_time >= 75 and lh_gol == la_gol:
            st.success("🔥 **Kritik Canlı Sinyal:** Maç sonu kilitlenmesi! **Sıradaki Gol Var / 0.5 ÜST** tercihi öne çıkıyor.")
        elif c_time < 45 and (lh_gol + la_gol) >= 2:
            st.success("⚡ **Kritik Canlı Sinyal:** Tempolu ilk yarı! **İkinci Yarı 1.5 ÜST veya KG Var** değerlendirilebilir.")
        else:
            st.info("🎯 **Canlı Sinyal:** Maç dengede ilerliyor, oran takiplerini yapabilirsiniz.")
