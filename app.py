import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="UHRE Master Portal", layout="wide")

@st.cache_data
def load_data():
    # List all files in the folder to see what Streamlit sees
    files = os.listdir('.')
    
    # Try to find any Excel file if 'data.xlsx' isn't found
    target = 'data.xlsx'
    if target not in files:
        excel_files = [f for f in files if f.endswith('.xlsx') or f.endswith('.xlsm')]
        if excel_files:
            target = excel_files[0]
        else:
            return None, f"No Excel file found. I see: {files}"

    try:
        df = pd.read_excel(target, engine='openpyxl')
        df.columns = [str(c).replace('\n', ' ').strip() for c in df.columns]
        return df, None
    except Exception as e:
        return None, str(e)

df, error = load_data()

st.title("🏙️ UHRE Master Project Database")

if df is not None:
    # --- UI SEARCH ---
    search = st.text_input("🔍 Search Projects")
    
    filtered = df.copy()
    if search:
        mask = filtered.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)
        filtered = filtered[mask]

    st.write(f"Showing {len(filtered)} items")

    for _, row in filtered.iterrows():
        p_name = str(row.get('Project Name', 'Unnamed'))
        if p_name.lower() in ['nan', 'none', 'project name']: continue
        
        # Look for the link
        link = None
        for val in row:
            if "drive.google.com" in str(val):
                link = str(val)
                break

        with st.container():
            st.markdown(f"""
                <div style="background:white; padding:20px; border-radius:12px; border:1px solid #eee; border-left:6px solid #1E3A8A; margin-bottom:15px; color:black;">
                    <h3 style="margin:0;">{p_name}</h3>
                    <p style="margin:5px 0;">🏢 {row.get('Developer', 'N/A')} | 📍 {row.get('Community/Area', 'N/A')}</p>
                    <a href="{link if link else '#'}" target="_blank" style="display:inline-block; padding:10px 20px; background:#1E3A8A; color:white; border-radius:5px; text-decoration:none;">📂 Open Pack</a>
                </div>
            """, unsafe_allow_html=True)
else:
    st.error(f"⚠️ App could not start: {error}")
    st.write("Please check your GitHub file names.")
