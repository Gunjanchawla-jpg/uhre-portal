import streamlit as st
import pandas as pd

st.set_page_config(page_title="UHRE Master Portal", layout="wide")

@st.cache_data
def load_data():
    # We use 'latin-1' because it is the most 'forgiving' encoding for Excel CSVs
    try:
        df = pd.read_csv(
            'data.csv', 
            encoding='latin-1', 
            on_bad_lines='skip', 
            encoding_errors='ignore',
            sep=None, # This tells pandas to guess if you used commas or semicolons
            engine='python'
        )
        # Clean column names
        df.columns = df.columns.str.replace(r'\n', ' ', regex=True).str.strip()
        return df
    except Exception as e:
        st.error(f"Ultimate Load Failed: {e}")
        return None

df = load_data()

st.title("🏙️ UHRE Master Project Database")

if df is not None:
    # Let's make sure we are actually seeing the columns
    search = st.text_input("🔍 Search by Developer, Area, or Project")
    
    filtered = df.copy()
    if search:
        mask = filtered.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)
        filtered = filtered[mask]

    for _, row in filtered.iterrows():
        # Using a safer way to get data to prevent crashes
        p_name = row.get('Project Name', 'Unnamed Project')
        dev = row.get('Developer', 'N/A')
        area = row.get('Community/Area', 'N/A')
        
        # Look for the Google Drive link column specifically
        link_col = [c for c in df.columns if 'Agent Pack' in c or 'Link' in c]
        link = row[link_col[0]] if link_col and pd.notnull(row[link_col[0]]) else "#"

        st.markdown(f"""
            <div style="background:white; padding:20px; border-radius:12px; border-left:6px solid #1E3A8A; box-shadow:0 4px 6px rgba(0,0,0,0.1); margin-bottom:15px;">
                <h3 style="margin:0; color:#1E3A8A;">{p_name}</h3>
                <p><b>{dev}</b> | {area}</p>
                <a href="{link}" target="_blank" style="color:#1E3A8A; font-weight:bold; text-decoration:none;">📂 View Marketing Assets</a>
            </div>
        """, unsafe_allow_html=True)
else:
    st.warning("Still unable to parse the file. Try resaving the file as 'CSV UTF-8' in Excel.")
