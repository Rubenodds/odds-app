python
import streamlit as st

# Tvinger appen til at ignorere dvaletilstand i mobilbrowsere
if not st.session_state.get("init"):
    st.session_state["kampe"] = []
    st.session_state["init"] = True

st.set_page_config(page_title="AI Multi-Optimizer", page_icon="⚽")

st.title("⚽ AI Oddset Multi-Optimizer")
st.write("Indtast dine kampe for at bygge kuponen. Denne udgave er dvalesikret til mobilen.")

# Strategi - Gemmes i session, så skærmskift ikke nulstiller
st.header("🎯 1. Vælg din Kupon-Strategi")
odds_niveau = st.selectbox("Strategi", ["Sikker (Odds 5+)", "Medium (Odds 30+)", "Højrisiko (Odds 70+)", "Giga-Kupon (Odds 300+)"])
min_odds = st.slider("Mindste odds pr. kamp", 1.10, 3.00, 1.50, step=0.05)

# Formular
st.header("📋 2. Tilføj Kamp")
with st.form("kamp_form", clear_on_submit=True):
    liga = st.text_input("Liga", "Champions League")
    hjemme = st.text_input("Hjemmehold")
    ude = st.text_input("Udehold")
    h_form = st.slider("Hjemmeholdets form (1-10)", 1, 10, 5)
    u_form = st.slider("Udeholdets form (1-10)", 1, 10, 5)
    tilfoej = st.form_submit_button("➕ Tilføj kamp")
    
    if tilfoej and hjemme and ude:
        st.session_state["kampe"].append({"liga": liga, "hjemme": hjemme, "ude": ude, "h_form": h_form, "u_form": u_form})
        st.success(f"Tilføjede {hjemme} vs. {ude}!")

# Vis kampe og beregn
if st.session_state["kampe"]:
    st.header("🏟️ Dine valgte kampe")
    for i, k in enumerate(st.session_state["kampe"]):
        st.write(f"{i+1}. [{k['liga']}] {k['hjemme']} vs. {k['ude']}")
        
    if st.button("❌ Nulstil kupon"):
        st.session_state["kampe"] = []
        st.rerun()

    if st.button("🔮 Beregn og optimer", type="primary"):
        st.subheader("📊 Dine AI Forslag")
        samlet_odds = 1.0
        for k in st.session_state["kampe"]:
            if odds_niveau == "Sikker (Odds 5+)":
                spil, o = "Over 1.5 mål", max(min_odds, 1.25)
            elif odds_niveau == "Medium (Odds 30+)":
                spil, o = "Begge hold scorer (Ja)", max(min_odds, 1.65)
            elif odds_niveau == "Højrisiko (Odds 70+)":
                spil, o = f"Byg Væddemål: {k['hjemme']}-sejr + Over 1.5 mål", max(min_odds, 2.10)
            else:
                spil, o = f"Byg Væddemål: {k['hjemme']}-sejr + Begge hold scorer", max(min_odds, 3.40)
                
            st.write(f"🎯 **{k['hjemme']} vs {k['ude']}:** {spil} (Odds {o:.2f})")
            samlet_odds *= o
        st.write(f"🔥 **Anslået samlet odds: {samlet_odds:.2f}**")
