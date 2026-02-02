import streamlit as st
import pandas as pd

st.set_page_config(page_title="UHRE Master Portal", layout="wide")

@st.cache_data
def load_data():
    try:
        # We use openpyxl because it is better at reading "hidden" link data
        df = pd.read_excel('data.csv', engine='openpyxl')
    except:
        df = pd.read_csv('data.csv', encoding='latin-1', on_bad_lines='skip')
    
    # Clean the column names (removes the \n and extra spaces)
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

    # Find the link column name - your file has a very specific one
    link_col_name = next((c for c in df.columns if 'Agent Pack' in c or 'Drive' in c), None)

    for _, row in filtered.iterrows():
        p_name = str(row.get('Project Name', '')).strip()
        if p_name.lower() in ["nan", "project name", ""] or len(p_name) < 3:
            continue

        # --- THE DEEP LINK SCAN ---
        link = None
        # First, check our detected link column
        if link_col_name:
            val = str(row[link_col_name]).strip()
            if "http" in val or "drive." in val:
                link = val if val.startswith("http") else "https://" + val
        
        # Second, if still no link, scan the WHOLE row
        if not link:
            for col_val in row:
                v = str(col_val).strip()
                if "drive.google.com" in v:
                    link = v if v.startswith("http") else "https://" + v
                    break

        dev = str(row.get('Developer', 'N/A'))
        area = str(row.get('Community/Area', 'N/A'))
        h_date = str(row.get('Handover Date', 'TBC'))
        if h_date.lower() == "nan": h_date = "Contact for Details"

        st.markdown(f"""
            <div style="background:white; padding:20px; border-radius:12px; border-left:6px solid #1E3A8A; box-shadow:0 4px 6px rgba(0,0,0,0.1); margin-bottom:15px; color: black;">
                <h3 style="margin:0; color:#1E3A8A;">{p_name}</h3>
                <p style="margin:5px 0;">🏢 <b>{dev}</b> | 📍 {area}</p>
                <p style="margin:5px 0; font-size: 0.9em; color: #555;">📅 Handover: {h_date}</p>
                {"<a href='" + link + "' target='_blank' style='display:inline-block; margin-top:10px; padding:10px 20px; background-color:#1E3A8A; color:white !important; text-decoration:none; border-radius:6px; font-weight:bold;'>📂 Open Agent Pack</a>" if link else "<span style='color:#d32f2f; background:#ffebee; padding:4px 8px; border-radius:4px; font-size:0.8em;'>⚠️ Link missing in source file</span>"}
            </div>
        """, unsafe_allow_html=True)
