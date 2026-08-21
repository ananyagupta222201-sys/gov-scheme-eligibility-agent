import streamlit as st
from agents.matching_agent import match_schemes
from agents.explainer_agent import explain_eligibility
from agents.checklist_agent import build_checklist
from agents.guide_agent import generate_guide

st.set_page_config(page_title="Sarkari Yojana Eligibility Agent", page_icon="🇮🇳", layout="wide")

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #fff7ed 0%, #fef3c7 100%);
    }
    h1, h2, h3, p, span, label, .stMarkdown {
        color: #1e293b !important;
    }
    [data-testid="stCaptionContainer"] {
        color: #475569 !important;
    }
    h1 {
        color: #ea580c !important;
    }
    .stButton>button {
        background-color: #16a34a;
        color: white !important;
        font-weight: bold;
        border-radius: 8px;
    }
    div[data-testid="stMetric"] {
        background-color: white;
        padding: 10px;
        border-radius: 10px;
        border: 1px solid #fed7aa;
    }
    div[data-testid="stExpander"] {
        border: 1px solid #fed7aa;
        border-radius: 10px;
        background-color: white;
    }
    section[data-testid="stSidebar"] {
        background-color: #fff7ed;
    }
</style>
""", unsafe_allow_html=True)

st.title("🇮🇳 Sarkari Yojana Eligibility Agent")
st.caption("Central + Uttar Pradesh + Maharashtra government schemes ke liye eligibility check karo")
st.divider()

with st.sidebar:
    st.header("Apni details bharo")

    with st.form("profile_form"):
        occupation = st.selectbox("Occupation", ["farmer", "student", "unemployed", "any"])
        income = st.number_input("Annual Income (₹)", min_value=0, value=200000, step=10000)
        age = st.number_input("Age", min_value=0, max_value=100, value=25)
        state = st.selectbox("State", ["Uttar Pradesh", "Maharashtra"])
        gender = st.selectbox("Gender", ["male", "female"])

        st.markdown("**Optional (aap chahen toh hi bharo)**")
        disclose_category = st.checkbox("Category disclose karna chahenge?")
        category = None
        if disclose_category:
            category = st.selectbox("Category", ["SC", "ST", "OBC", "EWS", "General"])

        has_disability = st.checkbox("Disability hai (80%+ certified)")

        submitted = st.form_submit_button("🔍 Check Eligibility", use_container_width=True)

if submitted:
    profile = {
        "occupation": occupation,
        "income": income,
        "age": age,
        "state": state,
        "gender": gender,
        "category": category,
        "has_disability": has_disability
    }

    matched = match_schemes(profile)

    if not matched:
        st.warning("Koi scheme match nahi hui. Apni details check karo.")
    else:
        st.success(f"✅ {len(matched)} schemes mili jo aap ke liye relevant ho sakti hain!")

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Matches", len(matched))
        col2.metric("Central Schemes", len([s for s in matched if s["level"] == "central"]))
        col3.metric("State Schemes", len([s for s in matched if s["level"] == "state"]))

        st.divider()

        for scheme in matched:
            with st.expander(f"📋 {scheme['name']}"):
                st.write(scheme["description"])
                with st.spinner("Explanation generate ho raha hai..."):
                    explanation = explain_eligibility(scheme, profile)
                st.info(explanation)

                st.markdown("**Documents needed:**")
                for doc in scheme["documents"]:
                    st.markdown(f"- {doc}")

                st.markdown("**Application Guide:**")
                with st.spinner("Guide generate ho raha hai..."):
                    guide = generate_guide(scheme)
                st.success(guide)

        st.divider()
        st.subheader("📄 Combined Document Checklist")
        checklist = build_checklist(matched)
        for doc, schemes_needing in checklist.items():
            st.checkbox(f"{doc}  _(needed for {len(schemes_needing)} scheme(s))_", key=doc)
else:
    st.info("👈 Sidebar mein apni details bharo aur 'Check Eligibility' button dabao.")