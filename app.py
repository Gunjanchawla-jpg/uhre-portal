import streamlit as st
import pandas as pd

st.set_page_config(page_title="UHRE Master Portal", layout="wide")

@st.cache_data
def load_data():
    try:
        # Try Excel first as it handles hidden data better
        df = pd.read_excel('data.csv', engine='openpyxl')
    except:
        df = pd.read_csv('data.csv', encoding='latin-1', on_bad_lines='skip', encoding_errors='ignore')
    
    # Clean the column names
    df.columns = [str(c).replace('\n', ' ').strip() for c in df.columns]
    return df

df = load_data()

st.title("🏙️ UHRE Master Project Database")

if df is not None:
    search = st.text_input("🔍 Search Projects (e.g. Emaar, Dubailand, Magenta)")

    filtered = df.copy()
    if search:
        mask = filtered.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)
        filtered = filtered[mask]

    st.write(f"Showing {len(filtered)} items")

    for _, row in filtered.iterrows():
        p_name = str(row.get('Project Name', '')).strip()
        # Skip empty rows or header rows
        if p_name.lower() in ["nan", "project name", ""] or len(p_name) < 3:
            continue

        # --- THE SMART LINK FINDER ---
        link = None
        for col_val in row:
            val_str = str(col_val).strip()
            # Check if the cell looks like a link
            if "http" in val_str or "drive.google" in val_str or "bit.ly" in val_str:
                # If it's a link but missing http, add it so the button works
                if not val_str.startswith('http') and "drive." in val_str:
                    link = "https://" + val_str
                else:
                    link = val_str
                break
        
        dev = row.get('Developer', 'N/A')
        area = row.get('Community/Area', 'N/A')
        handover = row.get('Handover Date', 'TBC')

        st.markdown(f"""
            <div style="background:white; padding:20px; border-radius:12px; border-left:6px solid #1E3A8A; box-shadow:0 4px 6px rgba(0,0,0,0.1); margin-bottom:15px; color: black;">
                <h3 style="margin:0; color:#1E3A8A;">{p_name}</h3>
                <p style="margin:5px 0;">🏢 <b>{dev}</b> | 📍 {area}</p>
                <p style="margin:5px 0; font-size: 0.9em; color: #555;">📅 Handover: {handover}</p>
                {"<a href='" + link + "' target='_blank' style='display:inline-block; margin-top:10px; padding:8px 18px; background-color:#1E3A8A; color:white !important; text-decoration:none; border-radius:6px; font-weight:bold;'>📂 Open Agent Pack</a>" if link else "<span style='color:red; font-size:0.8em;'>⚠️ No Link Found in Row</span>"}
            </div>
        """, unsafe_allow_html=True)
else:
    st.error("Data file missing.")
