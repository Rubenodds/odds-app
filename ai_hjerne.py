import sqlite3
import random

# Initialiserer en lokal database i din mappe, der husker alt permanent
def init_database():
    conn = sqlite3.connect("odds_hukommelse.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS historik (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dato TEXT,
            liga TEXT,
            hjemmehold TEXT,
            udehold TEXT,
            spilforslag TEXT,
            odds REAL,
            status TEXT DEFAULT 'Afventer'
        )
    """)
    conn.commit()
    conn.close()

# Funktion der bygger autopilot-kuponen baseret på dit målsatte odds
def generer_ai_kupon(maal_odds, antal_kampe):
    # Den absolut komplette pulje af ligaer fra alle dine billeder!
    pulje = [
        ("Premier League", "Man City", "Arsenal", "Over 2.5 mål", 1.65),
        ("Premier League", "Liverpool", "Chelsea", "Ren Liverpool-sejr", 1.72),
        ("Championship (England)", "Leeds", "Burnley", "Dobbeltchance: Hjemme eller Uafgjort", 1.30),
        ("League One (England)", "Bolton", "Portsmouth", "Over 1.5 mål", 1.25),
        ("League Two (England)", "Wrexham", "Stockport", "Begge hold scorer (Ja)", 1.60),
        ("FA Cup", "Man United", "Newcastle", "Over 2.5 mål", 1.65),
        ("EFL Cup", "Tottenham", "West Ham", "Ren Tottenham-sejr", 1.80),
        ("Superligaen", "FCK", "Brøndby", "Dobbeltchance: FCK eller Uafgjort", 1.30),
        ("Superligaen", "FC Midtjylland", "AGF", "Ren FCM-sejr", 1.85),
        ("Betinia LIGA (1. div)", "OB", "Esbjerg", "Ren OB-sejr", 1.55),
        ("CampoBet 2. Division", "Fremad Amager", "Aarhus Fremad", "Over 2.5 mål", 1.68),
        ("Betano Pokalen", "Silkeborg", "Viborg", "Begge hold scorer (Ja)", 1.60),
        ("LaLiga", "Real Madrid", "Barcelona", "Begge hold scorer + Over 2.5 mål", 1.80),
        ("LaLiga2", "Espanyol", "Zaragoza", "Under 2.5 mål i kampen", 1.55),
        ("Copa del Rey", "Athletic Bilbao", "Real Betis", "Dobbeltchance: Hjemme eller Uafgjort", 1.40),
        ("Premiership (Skotland)", "Celtic", "Rangers", "Over 2.5 mål", 1.60),
        ("Allsvenskan (Sverige)", "Malmö FF", "Hammarby", "Ren Malmö-sejr", 1.75),
        ("Super Lig (Tyrkiet)", "Galatasaray", "Fenerbahce", "Begge hold scorer (Ja)", 1.62),
        ("Bundesliga (Tyskland)", "Bayern München", "Dortmund", "Over 3.5 mål i kampen", 1.95),
        ("2. Bundesliga", "Hamburger SV", "Schalke 04", "Over 2.5 mål", 1.65),
        ("3. Liga (Tyskland)", "Dynamo Dresden", "Rostock", "Ren hjemmesejr", 1.90),
        ("MLS (USA)", "Inter Miami", "LA Galaxy", "Over 3.5 mål i kampen", 2.10),
        ("Bundesliga (Østrig)", "Salzburg", "Sturm Graz", "Ren Salzburg-sejr", 1.68),
        ("Serie B (Italien)", "Palermo", "Sampdoria", "Dobbeltchance: Hjemme eller Uafgjort", 1.38),
        ("Coppa Italia", "Juventus", "Lazio", "Ren Juventus-sejr", 1.75),
        ("J2 League (Japan)", "Yokohama FC", "Chiba", "Over 2.5 mål", 1.82),
        ("Eliteserien (Norge)", "Bodø/Glimt", "Molde", "Begge hold scorer (Ja)", 1.50),
        ("Liga Portugal", "Benfica", "Sporting CP", "Over 2.5 mål", 1.68),
        ("Superliga (Rumænien)", "FCSB", "CFR Cluj", "Under 2.5 mål i kampen", 1.62),
        ("Super League (Schweiz)", "Young Boys", "Basel", "Over 2.5 mål", 1.55),
        ("Super Liga (Serbien)", "Røde Stjerne", "Partizan", "Ren Røde Stjerne-sejr", 1.45),
        ("Ligue 1 (Frankrig)", "PSG", "Marseille", "Ren PSG-sejr", 1.50),
        ("Ligue 2 (Frankrig)", "Auxerre", "Bordeaux", "Over 1.5 mål", 1.28),
        ("Ligue 3 (Frankrig)", "Red Star", "Niort", "Ren hjemmesejr", 1.85),
        ("Coupe de France", "Lyon", "Nice", "Begge hold scorer (Ja)", 1.65),
        ("Super League (Grækenland)", "Olympiakos", "Panathinaikos", "Under 2.5 mål", 1.70),
        ("Æresdivisionen (Holland)", "Ajax", "PSV", "Over 2.5 mål", 1.58),
        ("1. division (Holland)", "Groningen", "Breda", "Ren hjemmesejr", 1.62),
        ("Besta-deild karla (Island)", "Vikingur", "Valur", "Over 3.5 mål", 2.15),
        ("Serie A (Italien)", "Inter", "Juventus", "Dobbeltchance: Inter eller Uafgjort", 1.32),
        ("A-League (Australien)", "Sydney FC", "Melbourne Victory", "Over 2.5 mål", 1.60),
        ("Jupiler League (Belgien)", "Club Brügge", "Anderlecht", "Ren hjemmesejr", 1.75),
        ("Serie A (Brasilien)", "Palmeiras", "Flamengo", "Under 2.5 mål", 1.65),
        ("Serie B (Brasilien)", "Santos", "Coritiba", "Ren Santos-sejr", 1.50),
        ("Parva Liga (Bulgarien)", "Ludogorets", "CSKA Sofia", "Ren hjemmesejr", 1.40),
        ("Premier League (Egypten)", "Al Ahly", "Zamalek", "Dobbeltchance: Al Ahly eller Uafgjort", 1.25),
        ("EM", "Danmark", "Tyskland", "Over 1.5 mål", 1.30),
        ("Champions League", "Real Madrid", "Man City", "Begge hold scorer (Ja)", 1.52),
        ("Europa League", "Roma", "Ajax", "Dobbeltchance: Roma eller Uafgjort", 1.35),
        ("Conference League", "Fiorentina", "Real Betis", "Over 2.5 mål", 1.75),
        ("UEFA Nations League", "Spanien", "Frankrig", "Begge hold scorer (Ja)", 1.68),
        ("Veikkausliiga (Finland)", "HJK Helsinki", "KuPS", "Ren HJK-sejr", 1.80)
    ]
    
    antal = min(antal_kampe, len(pulje))
    valgte_kampe = random.sample(pulje, antal)
    
    kupon_liste = []
    samlet_odds = 1.0
    
    for liga, hj, ud, spil, o in valgte_kampe:
        justering = (maal_odds / 30.0) ** (1 / antal)
        if justering < 0.8: justering = 0.8
        if justering > 2.5: justering = 2.5
        
        nyt_odds = round(o * justering, 2)
        if nyt_odds < 1.15: nyt_odds = 1.15
        
        kupon_liste.append({
            "liga": liga, "hjemme": hj, "ude": ud, "spil": spil, "odds": nyt_odds
        })
        samlet_odds *= nyt_odds
        
    return kupon_liste, round(samlet_odds, 2)

# Funktion til at gemme en kupon i historikken
def gem_kupon_i_historik(dato, liga, hj, ud, spil, o, status):
    conn = sqlite3.connect("odds_hukommelse.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO historik (dato, liga, hjemmehold, udehold, spilforslag, odds, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (dato, liga, hj, ud, spil, o, status))
    conn.commit()
    conn.close()
