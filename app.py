import streamlit as st

st.set_page_config(page_title="AI Oddset Multi-Optimizer", page_icon="⚽", layout="centered")

st.title("⚽ AI Oddset Multi-Optimizer")
st.write("Byg kuponer fra odds 5 til over 300+ med kontrol over minimums-odds.")

if "kampe" not in st.session_state:
    st.session_state.kampe = []

st.header("🎯 1. Indstil din Kupon-Strategi")
col_strat1, col_strat2 = st.columns(2)
with col_strat1:
    odds_niveau = st.select_slider(
        "Hvor vild skal kuponen være?",
        options=["Sikker (Odds 5+)", "Medium (Odds 30+)", "Højrisiko (Odds 70+)", "Giga-Kupon (Odds 300+)"]
    )
with col_strat2:
    min_odds_krav = st.slider("Minimums-odds pr. kamp", 1.10, 3.00, 1.50, step=0.05)

st.header("📋 2. Tilføj Kamp")
with st.form("kamp_form", clear_on_submit=True):
    liga = st.text_input("Turnering / Liga", placeholder="F.eks. Premier League, CL")
    hjemme = st.text_input("Hjemmehold", placeholder="F.eks. Real Madrid")
    ude = st.text_input("Udehold", placeholder="F.eks. Barcelona")
    
    st.write("**Styrkeforhold (1-10)**")
    col1, col2 = st.columns(2)
    with col1:
        h_form = st.slider("Hjemmeholdets form/niveau", 1, 10, 5)
        h_maal = st.number_input("Hjemmeholdets målsnit", 0.0, 5.0, 1.5, step=0.1)
    with col2:
        u_form = st.slider("Udeholdets form/niveau", 1, 10, 5)
        u_maal = st.number_input("Udeholdets målsnit", 0.0, 5.0, 1.5, step=0.1)
    forventede_kort = st.slider("Forventet tænding/kort i kampen", 1, 10, 4)
    tilfoej = st.form_submit_button("➕ Tilføj kamp til kuponen")
    
    if tilfoej and hjemme and ude:
        st.session_state.kampe.append({
            "liga": liga, "hjemme": hjemme, "ude": ude,
            "h_form": h_form, "u_form": u_form,
            "h_maal": h_maal, "u_maal": u_maal, "kort": forventede_kort
        })
        st.success(f"Tilføjede {hjemme} vs. {ude}!")

if st.session_state.kampe:
    st.header("🏟️ Dine valgte kampe")
    for i, k in enumerate(st.session_state.kampe):
        st.write(f"**{i+1}. [{k['liga']}] {k['hjemme']} vs. {k['ude']}**")
    if st.button("❌ Nulstil og tøm kupon"):
        st.session_state.kampe = []
        st.rerun()

    st.header("🎲 3. AI Kupon-Generering")
    if st.button("🔮 Beregn og optimer væddemål", type="primary"):
        genereret_kupon = []
        samlet_odds = 1.0
        for k in st.session_state.kampe:
            h_styrke = k["h_form"] + (k["h_maal"] * 1.5)
            u_styrke = k["u_form"] + (k["u_maal"] * 1.5)
            spil, o = "Over 1.5 mål", 1.25
            
            if odds_niveau == "Sikker (Odds 5+)":
                if abs(h_styrke - u_styrke) < 2: spil, o = "Over 1.5 mål i kampen", 1.25
                elif h_styrke > u_styrke: spil, o = f"Dobbeltchance: {k['hjemme']} eller Uafgjort", 1.22
                else: spil, o = f"Dobbeltchance: {k['ude']} eller Uafgjort", 1.22
            elif odds_niveau == "Medium (Odds 30+)":
                if h_styrke > u_styrke + 3: spil, o = f"Ren {k['hjemme']}-sejr", 1.55
                elif u_styrke > h_styrke + 3: spil, o = f"Ren {k['ude']}-sejr", 1.55
                else: spil, o = "Begge hold scorer (Ja)", 1.65
            elif odds_niveau == "Højrisiko (Odds 70+)":
                if h_styrke > u_styrke + 3: spil, o = f"Byg Væddemål: {k['hjemme']}-sejr + Over 1.5 mål", 1.95
                elif h_styrke > u_styrke: spil, o = f"Byg Væddemål: {k['hjemme']}-sejr + Begge hold scorer", 2.90
                else: spil, o = f"Byg Væddemål: {k['ude']}-sejr + Begge hold scorer", 3.40
            else:
                if h_styrke > u_styrke + 4: spil, o = f"Handicap: {k['hjemme']} vinder med 2+ mål (-1)", 2.40
                elif h_styrke > u_styrke: spil, o = f"Byg Væddemål: {k['hjemme']}-sejr + Begge hold scorer + Over 2.5 mål", 4.50
                else: spil, o = f"Byg Væddemål: {k['ude']}-sejr + Begge hold scorer + Over 2.5 mål", 4.80

            if o < min_odds_krav:
                if "Dobbeltchance" in spil or "Over 1.5" in spil:
                    spil, o = f"Byg Væddemål: {spil} + Over 2.5 mål", max(min_odds_krav + 0.15, 1.65)
                elif "Ren" in spil:
                    hold_navn = k['hjemme'] if h_styrke > u_styrke else k['ude']
                    spil, o = f"Byg Væddemål: {hold_navn}-sejr + Begge hold scorer", max(min_odds_krav + 0.40, 2.80)

            genereret_kupon.append(f"🎯 **{k['hjemme']} vs {k['ude']}:** {spil} (Odds {o:.2f})")
            samlet_odds *= o

        st.subheader(f"📊 Dine Indstillinger")
        st.write(f"Niveau: **{odds_niveau}** | Mindste odds pr. kamp: **{min_odds_krav:.2f}**")
        st.write(f"🔥 **Anslået samlet odds for kuponen: {samlet_odds:.2f}**")
        for valg in genereret_kupon:
            st.write(valg)
else:
    st.info("Tilføj kampe ovenfor for at begynde at bygge dine kuponer.")
