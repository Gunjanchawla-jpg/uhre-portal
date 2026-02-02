import streamlit as st
import pandas as pd

st.set_page_config(page_title="UHRE Master Portal", layout="wide")

@st.cache_data
def load_data():
    try:
        # We try reading it as an Excel file first, even if it says .csv
        # This fixes the "garbage text" issue
        df = pd.read_excel('data.csv', engine='openpyxl')
    except:
        try:
            # Fallback if it actually IS a CSV
            df = pd.read_csv('data.csv', encoding='latin-1', on_bad_lines='skip')
        except:
            return None

    # Clean column names
    df.columns = [str(c).replace('\n', ' ').strip() for c in df.columns]
    
    # Remove empty rows and repeated headers
    df = df.dropna(subset=[df.columns[1], df.columns[2]], how='all')
    return df

df = load_data()

st.title("🏙️ UHRE Master Project Database")

if df is not None:
    search = st.text_input("🔍 Search Projects (Developer, Area, or Name)")

    # Define the columns we want to show
    # We use list search to find the right columns in your file
    col_name = next((c for c in df.columns if 'Project' in c), df.columns[1])
    col_area = next((c for c in df.columns if 'Area' in c or 'Community' in c), df.columns[2])
    col_dev = next((c for c in df.columns if 'Developer' in c), df.columns[3])
    col_link = next((c for c in df.columns if 'Drive' in c or 'Pack' in c or 'Link' in c), df.columns[4])

    filtered = df.copy()
    if search:
        mask = filtered.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)
        filtered = filtered[mask]

    st.write(f"Showing {len(filtered)} items")

    for _, row in filtered.iterrows():
        p_name = str(row[col_name])
        if p_name.lower() in ["nan", "project name", "none"] or len(p_name) < 2:
            continue

        st.markdown(f"""
            <div style="background:white; padding:20px; border-radius:12px; border-left:6px solid #1E3A8A; box-shadow:0 4px 6px rgba(0,0,0,0.1); margin-bottom:15px; color: black;">
                <h3 style="margin:0; color:#1E3A8A;">{p_name}</h3>
                <p style="margin:5px 0;">🏢 <b>{row.get(col_dev, 'N/A')}</b> | 📍 {row.get(col_area, 'N/A')}</p>
                <a href="{row.get(col_link, '#')}" target="_blank" style="display:inline-block; margin-top:10px; padding:8px 15px; background-color:#1E3A8A; color:white; text-decoration:none; border-radius:5px; font-weight:bold;">📂 Open Agent Pack</a>
            </div>
        """, unsafe_allow_html=True)
else:
    st.error("Format error: Please ensure data.csv is a valid Excel or CSV file.")
