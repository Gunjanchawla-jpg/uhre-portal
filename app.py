import streamlit as st
import pandas as pd

st.set_page_config(page_title="UHRE Master Portal", layout="wide")

@st.cache_data
def load_data():
    try:
        # Trying Excel first as it handles the symbols better
        df = pd.read_excel('data.csv', engine='openpyxl')
    except:
        df = pd.read_csv('data.csv', encoding='latin-1', on_bad_lines='skip', encoding_errors='ignore')
    
    # Clean the column names for easier searching
    df.columns = [str(c).replace('\n', ' ').strip() for c in df.columns]
    return df

df = load_data()

st.title("🏙️ UHRE Master Project Database")

if df is not None:
    search = st.text_input("🔍 Search Projects (Developer, Area, or Name)")

    # Filter data first
    filtered = df.copy()
    if search:
        mask = filtered.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)
        filtered = filtered[mask]

    st.write(f"Showing {len(filtered)} items")

    for _, row in filtered.iterrows():
        # 1. Identify Project Name
        p_name = str(row.get('Project Name', 'Unnamed Project')).strip()
        if p_name.lower() in ["nan", "project name", "none"] or len(p_name) < 2:
            continue

        # 2. FIND THE LINK (The "Magic" part)
        # This scans every column in the row to find a link starting with 'http'
        link = None
        for val in row:
            val_str = str(val).strip()
            if val_str.startswith('http'):
                link = val_str
                break

        # 3. Get other details
        dev = row.get('Developer', 'N/A')
        area = row.get('Community/Area', 'N/A')

        st.markdown(f"""
            <div style="background:white; padding:20px; border-radius:12px; border-left:6px solid #1E3A8A; box-shadow:0 4px 6px rgba(0,0,0,0.1); margin-bottom:15px; color: black;">
                <h3 style="margin:0; color:#1E3A8A;">{p_name}</h3>
                <p style="margin:5px 0;">🏢 <b>{dev}</b> | 📍 {area}</p>
                {"<a href='" + link + "' target='_blank' style='display:inline-block; margin-top:10px; padding:8px 15px; background-color:#1E3A8A; color:white; text-decoration:none; border-radius:5px; font-weight:bold;'>📂 Open Agent Pack</a>" if link else "<i style='color:gray;'>No link detected in this row</i>"}
            </div>
        """, unsafe_allow_html=True)
else:
    st.error("Please ensure data.csv is uploaded to GitHub.")
