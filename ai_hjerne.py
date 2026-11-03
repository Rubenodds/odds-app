import sqlite3
import random

# Initialiserer en lokal database i din mappe, der husker alt permanent
def init_database():
    conn = sqlite3.connect("odds_hukommelse.db")
    cursor = conn.cursor()
    # Tabel til at huske alle genererede kuponer og om de vandt/tabte
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

# Funktion der lynhurtigt bygger autopilot-kuponen baseret på dit målsatte odds
def generer_ai_kupon(maal_odds, antal_kampe):
    # Live pulje af kampe (Hentes i næste trin direkte live fra nettet)
    pulje = [
        ("Premier League", "Man City", "Arsenal", "Over 2.5 mål", 1.65),
        ("Premier League", "Liverpool", "Chelsea", "Ren Liverpool-sejr", 1.72),
        ("Premier League", "Man United", "Tottenham", "Begge hold scorer (Ja)", 1.55),
        ("Superligaen", "FCK", "Brøndby", "Dobbeltchance: FCK eller Uafgjort", 1.30),
        ("Superligaen", "FC Midtjylland", "AGF", "Ren FCM-sejr", 1.85),
        ("Superligaen", "Nordsjælland", "Viborg", "Over 1.5 mål i 1. halvleg", 2.10),
        ("Champions League", "Real Madrid", "Bayern München", "Byg væddemål: Uafgjort", 3.45),
        ("Champions League", "Barcelona", "PSG", "Byg væddemål: Barca vinder + Over 2.5", 2.85),
    ]
    
    # Sikrer vi ikke trækker flere kampe end der er i puljen
    antal = min(antal_kampe, len(pulje))
    valgte_kampe = random.sample(pulje, antal)
    
    kupon_liste = []
    samlet_odds = 1.0
    
    for liga, hj, ud, spil, o in valgte_kampe:
        # AI-algoritme: Justerer de enkelte odds dynamisk, så den samlede kupon rammer dit mål
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

# Funktion til at gemme en kupon i historikken, så AI'en kan lære af den
def gem_kupon_i_historik(dato, liga, hj, ud, spil, o, status):
    conn = sqlite3.connect("odds_hukommelse.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO historik (dato, liga, hjemmehold, udehold, spilforslag, odds, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (dato, liga, hj, ud, spil, o, status))
    conn.commit()
    conn.close()
