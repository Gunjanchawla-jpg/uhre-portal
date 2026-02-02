import streamlit as st
import pandas as pd

st.set_page_config(page_title="UHRE Master Portal", layout="wide")

@st.cache_data
def load_data():
    try:
        # We only want the first 7 columns (Date, Project, Area, Dev, Link, Handover)
        # This prevents the 'Buffer overflow' caused by extra commas at the end of rows
        df = pd.read_csv(
            'data.csv', 
            encoding='latin-1', 
            on_bad_lines='skip', 
            encoding_errors='ignore',
            engine='python',
            # We skip the first row if it's a duplicate or use it as header
        )
        
        # Standardize column names
        df.columns = [str(c).replace('\n', ' ').strip() for c in df.columns]
        
        # Filter out rows that are just header repeats (like when you see 'Project Name' inside the data)
        if 'Project Name' in df.columns:
            df = df[df['Project Name'] != 'Project Name']
            
        return df
    except Exception as e:
        st.error(f"Structure Error: {e}")
        return None

df = load_data()

st.title("🏙️ UHRE Master Project Database")

if df is not None:
    search = st.text_input("🔍 Search Projects (Developer, Area, or Name)")

    # Find columns safely
    col_name = 'Project Name' if 'Project Name' in df.columns else df.columns[2]
    col_area = 'Community/Area' if 'Community/Area' in df.columns else df.columns[3]
    col_dev = 'Developer' if 'Developer' in df.columns else df.columns[4]
    
    # Smart search for the link column
    link_cols = [c for c in df.columns if 'Agent Pack' in c or 'Link' in c]
    col_link = link_cols[0] if link_cols else df.columns[5]

    filtered = df.copy()
    if search:
        mask = filtered.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)
        filtered = filtered[mask]

    # Show results
    for _, row in filtered.iterrows():
        # Skip empty rows
        if pd.isna(row[col_name]) or str(row[col_name]).strip() == "":
            continue

        st.markdown(f"""
            <div style="background:white; padding:20px; border-radius:12px; border-left:6px solid #1E3A8A; box-shadow:0 4px 6px rgba(0,0,0,0.1); margin-bottom:15px; color: black;">
                <h3 style="margin:0; color:#1E3A8A;">{row[col_name]}</h3>
                <p style="margin:5px 0;">🏢 <b>{row.get(col_dev, 'N/A')}</b> | 📍 {row.get(col_area, 'N/A')}</p>
                <p style="margin:5px 0;">📅 Handover: {row.get('Handover Date', 'Contact for Details')}</p>
                <a href="{row.get(col_link, '#')}" target="_blank" style="display:inline-block; margin-top:10px; padding:8px 15px; background-color:#1E3A8A; color:white; text-decoration:none; border-radius:5px; font-weight:bold;">📂 Open Agent Pack</a>
            </div>
        """, unsafe_allow_html=True)
else:
    st.info("The file 'data.csv' is being processed. Please refresh in 10 seconds.")
