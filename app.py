import streamlit as st
import pandas as pd

st.set_page_config(page_title="UHRE Master Portal", layout="wide")

@st.cache_data
def load_data():
    try:
        # Load the file with latin-1 to avoid encoding crashes
        df = pd.read_csv('data.csv', encoding='latin-1', on_bad_lines='skip', encoding_errors='ignore')
        
        # CLEANING: Remove completely empty rows and columns
        df = df.dropna(how='all', axis=0).dropna(how='all', axis=1)
        
        # Clean column names
        df.columns = [str(c).replace('\n', ' ').strip() for c in df.columns]
        
        # Remove rows that are just repeats of the header
        if 'Project Name' in df.columns:
            df = df[df['Project Name'] != 'Project Name']
            
        return df
    except Exception as e:
        st.error(f"Error: {e}")
        return None

df = load_data()

st.title("🏙️ UHRE Master Project Database")

if df is not None:
    # Search Box
    search = st.text_input("🔍 Search Projects (e.g., Emaar, Dubailand, Cove Edition)")

    # Identify the correct columns even if named slightly differently
    # Based on your file: 'Project Name', 'Community/Area', 'Developer', 'Agent Pack (Google Drive)'
    col_project = 'Project Name'
    col_area = 'Community/Area'
    col_dev = 'Developer'
    # Find the link column (it has a lot of spaces in your file)
    col_link = [c for c in df.columns if 'Agent Pack' in c or 'Link' in c][0]

    # Filtering logic
    filtered = df.copy()
    if search:
        mask = filtered.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)
        filtered = filtered[mask]

    # Displaying the Cards
    for _, row in filtered.iterrows():
        # Skip rows that don't have a project name
        if pd.isna(row[col_project]) or str(row[col_project]).strip() == "":
            continue

        name = row[col_project]
        developer = row.get(col_dev, "UHRE Project")
        area = row.get(col_area, "Dubai")
        link = row.get(col_link, "#")
        handover = row.get('Handover Date', 'Contact for Details')

        st.markdown(f"""
            <div style="background:white; padding:20px; border-radius:12px; border-left:6px solid #1E3A8A; box-shadow:0 4px 6px rgba(0,0,0,0.1); margin-bottom:15px; color: black;">
                <h3 style="margin:0; color:#1E3A8A;">{name}</h3>
                <p style="margin:5px 0;">🏢 <b>{developer}</b> | 📍 {area}</p>
                <p style="margin:5px 0;">📅 Handover: {handover}</p>
                <a href="{link}" target="_blank" style="display:inline-block; margin-top:10px; padding:8px 15px; background-color:#1E3A8A; color:white; text-decoration:none; border-radius:5px; font-weight:bold;">📂 Open Marketing Assets</a>
            </div>
        """, unsafe_allow_html=True)
else:
    st.error("Check your data.csv file on GitHub.")
