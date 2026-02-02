import streamlit as st
import pandas as pd

st.set_page_config(page_title="UHRE Agent Portal", layout="wide")

# This is the most important part for deployment
@st.cache_data
def load_data():
    try:
        # We use 'data.csv' because long names with spaces often break on the web
        df = pd.read_csv('data.csv')
        df.columns = df.columns.str.replace('\n', ' ').str.strip()
        return df
    except Exception as e:
        st.error(f"File Error: {e}")
        return None

df = load_data()

st.title("🏙️ UHRE Master Project Database")

if df is not None:
    search = st.text_input("🔍 Search Projects (e.g., Emaar, Dubailand, Magenta)")
    
    filtered = df.copy()
    if search:
        filtered = filtered[filtered.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)]

    for _, row in filtered.iterrows():
        with st.container():
            # This handles your specific column name from the CSV
            link = row.get('Agent Pack   (Google Drive)', '#')
            
            st.markdown(f"""
            <div style="background:white; padding:20px; border-radius:10px; border-left:6px solid #1E3A8A; box-shadow:0 2px 5px rgba(0,0,0,0.1); margin-bottom:15px;">
                <h3 style="margin:0;">{row['Project Name']}</h3>
                <p><b>{row['Developer']}</b> | {row['Community/Area']}</p>
                <p>📅 Handover: {row['Handover Date']}</p>
                <a href="{link}" target="_blank" style="color:#1E3A8A; font-weight:bold;">📂 Open Marketing Pack</a>
            </div>
            """, unsafe_allow_html=True)
