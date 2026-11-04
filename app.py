import math
import streamlit as st

st.set_page_config(
    page_title="ProBet AI - Gerçekçi İstatistik Merkezi",
    page_icon="⚽",
    layout="wide",
)

st.title("⚽ ProBet AI: Poisson & İstatistiksel Maç Analiz Motoru")
st.write("Harf toplamı gibi yanıltıcı yöntemler yerine; takımların gol ortalamaları ve gerçekçi form parametreleriyle çalışan profesyonel analiz paneli.")

tab1, tab2 = st.tabs(["📊 İstatistiksel Maç Analizi", "🔴 Canlı Maç Takip Paneli"])

def poisson_probability(lmbda, k):
    return (math.exp(-lmbda) * (lmbda ** k)) / math.factorial(k)

with tab1:
    st.subheader("1. Takım İstatistiklerini Girin (Maçkolik / SofaScore Verileri)")
    
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        home_name = st.text_input("Ev Sahibi Takım", value="Galatasaray", key="p_h_name")
        home_avg_scored = st.number_input("Ev Sahibinin Maç Başına Attığı Gol Ortalaması", 0.0, 5.0, 1.8, key="h_as")
        home_avg_conceded = st.number_input("Ev Sahibinin Maç Başına Yediği Gol Ortalaması", 0.0, 5.0, 0.8, key="h_ac")
    with col_t2:
        away_name = st.text_input("Deplasman Takımı", value="Fenerbahçe", key="p_a_name")
        away_avg_scored = st.number_input("Deplasmanın Maç Başına Attığı Gol Ortalaması", 0.0, 5.0, 1.5, key="a_as")
        away_avg_conceded = st.number_input("Deplasmanın Maç Başına Yediği Gol Ortalaması", 0.0, 5.0, 1.0, key="a_ac")

    if st.button("Bilimsel / İstatistiksel Analizi Çalıştır 🚀", type="primary", key="btn_poisson"):
        # Beklenen Gol (xG / Expected Goals) Hesaplaması
        home_exp = (home_avg_scored + away_avg_conceded) / 2 * 1.05  # Ev sahibi avantajı
        away_exp = (away_avg_scored + home_avg_conceded) / 2
        
        # En olası skorları bulmak için matris simülasyonu
        max_goals = 5
        best_prob = 0
        most_likely_score = (1, 1)
        
        home_win_prob = 0
        draw_prob = 0
        away_win_prob = 0
        
        score_matrix = {}
        for h in range(max_goals + 1):
            for a in range(max_goals + 1):
                p = poisson_probability(home_exp, h) * poisson_probability(away_exp, a)
                score_matrix[(h, a)] = p
                if h > a:
                    home_win_prob += p
                elif h == a:
                    draw_prob += p
                else:
                    away_win_prob += p
                
                if p > best_prob:
                    best_prob = p
                    most_likely_score = (h, a)

        total_p = home_win_prob + draw_prob + away_win_prob
        p1 = round((home_win_prob / total_p) * 100, 1)
        px = round((draw_prob / total_p) * 100, 1)
        p2 = round((away_win_prob / total_p) * 100, 1)

        # Oranlar
        o1 = round(100 / p1, 2) if p1 > 0 else 1.01
        ox = round(100 / px, 2) if px > 0 else 1.01
        o2 = round(100 / p2, 2) if p2 > 0 else 1.01

        st.success(f"📊 **{home_name} vs {away_name} — Poisson İstatistik Raporu**")

        # Yüzdeler
        m1, mx, m2, mc = st.columns(4)
        m1.metric(f"MS 1 (%{p1})", f"Oran: {o1}")
        mx.metric(f"MS X (%{px})", f"Oran: {ox}")
        m2.metric(f"MS 2 (%{p2})", f"Oran: {o2}")
        mc.metric("Gol Beklentisi (xG)", f"Ev: {round(home_exp, 2)} | Dep: {round(away_exp, 2)}")

        st.divider()

        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            st.write("**İstatistiksel Maç Sonucu**")
            if p1 > p2 and p1 > px:
                st.info(f"🎯 **MS 1 ({home_name} Favori)**")
            elif p2 > p1 and p2 > px:
                st.info(f"🎯 **MS 2 ({away_name} Favori)**")
            else:
                st.info("🎯 **Maç Beraberliğe Yakın (X)**")

        with col_b:
            st.write("**En Kuvvetli Skor Matrisi**")
            st.success(f"⚽ **{most_likely_score[0]} - {most_likely_score[1]}**")

        with col_c:
            st.write("**Alt / Üst & KG Durumu**")
            total_goals_exp = home_exp + away_exp
            au_res = "2.5 ÜST" if total_goals_exp > 2.4 else "2.5 ALT"
            kg_res = "KG Var" if most_likely_score[0] > 0 and most_likely_score[1] > 0 else "KG Yok"
            st.warning(f"🔥 {au_res}\n\n🤝 {kg_res}")

with tab2:
    st.subheader("🔴 Canlı Maç Takip Paneli")
    st.write("Devam eden maçın dakikasını ve skorunu girerek anlık analiz alın.")
    
    c_min = st.slider("Maç Dakikası", 1, 95, 70, key="live_time_poisson")
    lc1, lc2 = st.columns(2)
    with lc1:
        c_hg = st.number_input("Ev Sahibi Gol", 0, 10, 1, key="live_hg_poisson")
    with lc2:
        c_ag = st.number_input("Deplasman Gol", 0, 10, 1, key="live_ag_poisson")
        
    if st.button("Anlık Canlı Analiz Çalıştır ⚡", type="primary", key="btn_live_poisson"):
        st.warning(f"⏱️ Dakika: {c_min}' | Anlık Skor: {c_hg} - {c_ag}")
        if c_min >= 75 and c_hg == c_ag:
            st.success("🔥 **Canlı Sinyal:** Beraberlik bozulmadı! **Sıradaki Gol Var / 0.5 ÜST** değerlendirilebilir.")
        else:
            st.info("🎯 **Canlı Sinyal:** Oyun akışı normal seyrinde devam ediyor.")
