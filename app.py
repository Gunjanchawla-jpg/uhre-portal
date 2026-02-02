import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="UHRE Portal", layout="wide")

@st.cache_data
def load_data():
    # 1. Try the exact name first
    target_file = 'data.csv'
    
    # 2. If it's not found, look for ANY csv file in the folder
    if not os.path.exists(target_file):
        all_files = os.listdir('.')
        csv_files = [f for f in all_files if f.endswith('.csv')]
        if csv_files:
            target_file = csv_files[0] # Use the first CSV found
        else:
            return None, f"No CSV files found. Files seen: {all_files}"

    # 3. Try reading with different encodings
    for enc in ['utf-8', 'cp1252', 'latin1']:
        try:
            df = pd.read_csv(target_file, encoding=enc, on_bad_lines='skip', encoding_errors='ignore')
            # Clean columns
            df.columns = df.columns.str.replace(r'\n', ' ', regex=True).str.strip()
            return df, None
        except Exception:
            continue
    return None, "Encoding failed"

df, error_msg = load_data()

if df is not None:
    st.title("🏙️ UHRE Master Project Database")
    # ... (the rest of your search and card code from before)
    search = st.text_input("🔍 Search Projects")
    filtered = df.copy()
    if search:
        mask = filtered.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)
        filtered = filtered[mask]
    
    for _, row in filtered.iterrows():
        st.info(f"Project: {row.get('Project Name', 'N/A')}") # Simple test display
else:
    st.error(f"⚠️ {error_msg}")
    st.write("Current Folder Contents:", os.listdir('.'))
