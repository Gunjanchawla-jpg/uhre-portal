import streamlit as st
import pandas as pd

st.set_page_config(page_title="UHRE Master Portal", layout="wide")

@st.cache_data
def load_data():
    try:
        # We read the file without a header first to see what's inside
        df = pd.read_csv(
            'data.csv', 
            encoding='latin-1', 
            on_bad_lines='skip', 
            encoding_errors='ignore',
            sep=None, 
            engine='python'
        )
        
        # If the file is empty or tiny, stop here
        if df.empty:
            return None

        # Clean up column names
        df.columns = [str(c).replace('\n', ' ').strip() for c in df.columns]
        
        # Remove empty rows and columns
        df = df.dropna(how='all', axis=0)
        
        return df
    except Exception as e:
        st.error(f"Load Error: {e}")
        return None

df = load_data()

st.title("🏙️ UHRE Master Project Database")

if df is not None:
    search = st.text_input("🔍 Search Projects (Developer, Area, or Name)")

    # DYNAMIC COLUMN FINDER
    # We look for keywords since index numbers (like [2]) are failing
    def find_col(keywords, default_index):
        for col in df.columns:
            if any(key.lower() in col.lower() for key in keywords):
                return col
        return df.columns[default_index] if len(df.columns) > default_index else df.columns[0]

    col_name = find_col(['Project', 'Name'], 1)
    col_area = find_col(['Area', 'Community', 'Location'], 2)
    col_dev = find_col(['Developer', 'Dev'], 3)
    col_link = find_col(['Drive', 'Link', 'Agent Pack', 'Pack'], 4)

    filtered = df.copy()
    if search:
        # Search across all columns
        mask = filtered.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)
        filtered = filtered[mask]

    # Show results
    st.write(f"Showing {len(filtered)} items")
    
    for _, row in filtered.iterrows():
        # Check if we have a valid project name
        p_name = str(row.get(col_name, "")).strip()
        if p_name == "" or p_name.lower() == "nan" or p_name.lower() == "project name":
            continue

        st.markdown(f"""
            <div style="background:white; padding:20px; border-radius:12px; border-left:6px solid #1E3A8A; box-shadow:0 4px 6px rgba(0,0,0,0.1); margin-bottom:15px; color: black;">
                <h3 style="margin:0; color:#1E3A8A;">{p_name}</h3>
                <p style="margin:5px 0;">🏢 <b>{row.get(col_dev, 'N/A')}</b> | 📍 {row.get(col_area, 'N/A')}</p>
                <a href="{row.get(col_link, '#')}" target="_blank" style="display:inline-block; margin-top:10px; padding:8px 15px; background-color:#1E3A8A; color:white; text-decoration:none; border-radius:5px; font-weight:bold;">📂 Open Agent Pack</a>
            </div>
        """, unsafe_allow_html=True)
else:
    st.error("Could not read 'data.csv'. Please ensure it's a valid CSV file.")
