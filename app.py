import streamlit as st
import json
import os
from datetime import datetime

# --- JACOB KANE STANDARD THEME & CONFIG ---
st.set_page_config(page_title="DC Universe Codex", layout="wide")

# Custom CSS to mimic your provided HTML/CSS styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Crimson+Pro:wght@300;400&display=swap');
    
    html, body, [class*="st-"] {
        font-family: 'Crimson Pro', serif;
        background-color: #0d0b0f;
        color: #b8b0c8;
    }
    .stApp { background-color: #0d0b0f; }
    
    h1, h2, h3, .cinzel {
        font-family: 'Cinzel', serif;
        color: #c9a84c;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }
    
    .stButton>button {
        border: 1px solid #c9a84c !important;
        background-color: rgba(201,168,76,0.1) !important;
        color: #c9a84c !important;
        font-family: 'Cinzel', serif;
        border-radius: 0px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: rgba(201,168,76,0.2) !important;
        box-shadow: 0 0 10px rgba(201,168,76,0.3);
    }
    
    .data-card {
        padding: 20px;
        border-left: 3px solid #c9a84c;
        background-color: #1a1520;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- DATA PERSISTENCE ---
DB_FILE = "codex_storage.json"

def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding='utf-8') as f:
            return json.load(f)
    return {"Characters": {}, "Locations": {}}

def save_db(data):
    with open(DB_FILE, "w", encoding='utf-8') as f:
        json.dump(data, f, indent=4)

db = load_db()

# --- SIDEBAR NAVIGATION ---
st.sidebar.markdown("<h1 class='cinzel'>Codex</h1>", unsafe_allow_html=True)
nav = st.sidebar.radio("Navigate Vault", ["View Database", "Character Entry", "Location Entry", "Search & Export"])

# --- CHARACTER ENTRY (JACOB KANE STANDARD) ---
if nav == "Character Entry":
    st.markdown("<h2 class='cinzel'>Add New Character</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Entry Name (Unique ID)")
        aliases = st.text_input("Full Name / Aliases")
        affiliation = st.text_input("Affiliation")
        status = st.selectbox("Status", ["Active", "Deceased", "Incarcerated", "Unknown"])
    
    with col2:
        abilities = st.text_area("Abilities / Equipment")
        details = st.text_area("Additional Detail(s)")
        bio = st.text_area("Brief Character Bio (High-Density Description)")
        doc_link = st.text_input("Link To Google Docs Page")

    if st.button("SYNCHRONISE TO CODEX"):
        if name:
            db["Characters"][name] = {
                "Full Name / Aliases": aliases,
                "Affiliation": affiliation,
                "Status": status,
                "Abilities / Equipment": abilities,
                "Additional Detail(s)": details,
                "Brief Character Bio": bio,
                "Link To Google Docs": doc_link,
                "Last Modified": str(datetime.now().strftime("%Y-%m-%d"))
            }
            save_db(db)
            st.success(f"Character '{name}' recorded in the Codex.")
        else:
            st.error("Entry Name is required.")

# --- VIEW DATABASE ---
elif nav == "View Database":
    st.markdown("<h2 class='cinzel'>Global Archive</h2>", unsafe_allow_html=True)
    cat = st.selectbox("Category", ["Characters", "Locations"])
    
    if db[cat]:
        for key, info in db[cat].items():
            with st.expander(f"{key.upper()} | {info.get('Affiliation', 'N/A')}"):
                st.markdown(f"**Aliases:** {info.get('Full Name / Aliases')}")
                st.markdown(f"**Status:** {info.get('Status')}")
                st.markdown("---")
                st.markdown(f"**Abilities/Equipment:**\n{info.get('Abilities / Equipment')}")
                st.markdown(f"**Additional Details:**\n{info.get('Additional Detail(s)')}")
                st.markdown(f"**Brief Character Bio:**\n{info.get('Brief Character Bio')}")
                st.markdown(f"[Access Dossier]({info.get('Link To Google Docs')})")
                
                if st.button(f"Delete {key}", key=f"del_{key}"):
                    del db[cat][key]
                    save_db(db)
                    st.rerun()
    else:
        st.info("Archive is currently empty.")

# --- LOCATION ENTRY ---
elif nav == "Location Entry":
    st.markdown("<h2 class='cinzel'>Map New Location</h2>", unsafe_allow_html=True)
    loc_name = st.text_input("Location Name")
    districts = st.text_area("Districts / Subdistricts / Areas")
    shops = st.text_area("Notable Locations (Shops, Companies, & Landmarks)")
    landmarks = st.text_area("Key Landmarks")
    
    if st.button("MAP TO CODEX"):
        db["Locations"][loc_name] = {
            "Districts / Subdistricts / Areas": districts,
            "Notable Locations": shops,
            "Key Landmarks": landmarks
        }
        save_db(db)
        st.success(f"Location '{loc_name}' mapped.")
