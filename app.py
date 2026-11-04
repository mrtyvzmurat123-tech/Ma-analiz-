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
