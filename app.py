import streamlit as st
import datetime
import ai_hjerne

# Tvinger databasen til at vågne op
ai_hjerne.init_database()

st.set_page_config(page_title="AI Oddset Multi-Robot v2", page_icon="🤖", layout="centered")

st.title("🤖 AI Oddset Multi-Robot v2")
st.write("Fuldstændig dvalesikret, opdelt i professionelle moduler og koblet til databasehistorik.")

# 1. Autopilot-bygger via din nye ai_hjerne.py
st.header("🎯 Autopilot: Byg lynhurtig kupon")
col_auto1, col_auto2 = st.columns(2)
with col_auto1:
    mål_odds = st.number_input("Indtast målsat odds (f.eks. 10 eller 500)", min_value=2.0, max_value=1000.0, value=10.0, step=5.0)
with col_auto2:
    antal_kampe_auto = st.slider("Antal kampe på kuponen", 3, 12, 7)

if st.button("🔮 Generer Autopilot Kupon", type="primary"):
    st.info(f"Analyse i gang: Henter data og sammensætter odds {mål_odds:.2f}...")
    
    # Kalder din nye ai_hjerne.py og henter beregningerne derfra!
    kupon, samlet_odds = ai_hjerne.generer_ai_kupon(mål_odds, antal_kampe_auto)
    
    st.subheader(f"📋 Din genererede Odds {samlet_odds:.2f} autopilot-kupon:")
    for i, k in enumerate(kupon):
        st.write(f"⚽ **{i+1}. [{k['liga']}] {k['hjemme']} vs. {k['ude']}**")
        st.write(f" ➔ Spilforslag: **{k['spil']}** (Odds {k['odds']:.2f})")
        st.write("---")
        
        # Gemmer automatisk hver kamp i databasen, så den kan huske dem og lære af dem!
        ai_hjerne.gem_kupon_i_historik(str(datetime.date.today()), k['liga'], k['hjemme'], k['ude'], k['spil'], k['odds'], 'Afventer')
        
    st.success(f"🔥 Autopilot kupon klar og gemt i din database-histo")
