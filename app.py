import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="UHRE Agent Portal", layout="wide")

# 2. Custom Styling
st.markdown("""
    <style>
    .project-card {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        border-left: 6px solid #1E3A8A;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 15px;
    }
    .link-btn {
        background-color: #1E3A8A;
        color: white !important;
        padding: 8px 16px;
        border-radius: 6px;
        text-decoration: none;
        display: inline-block;
        margin-top: 10px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Data Loading with Encoding Fixes
@st.cache_data
def load_data():
    encodings = ['utf-8', 'cp1252', 'latin1']
    for enc in encodings:
        try:
            # We use 'data.csv' as the filename
            df = pd.read_csv('data.csv', encoding=enc, on_bad_lines='skip', encoding_errors='ignore')
            # Clean up the column names (removes the \n and extra spaces)
            df.columns = df.columns.str.replace(r'\n', ' ', regex=True).str.strip()
            return df
        except Exception:
            continue
    return None

# 4. Main App Logic
df = load_data()

st.title("🏙️ UHRE Master Project Database")

if df is not None:
    # Search Box
    search = st.text_input("🔍 Search by Developer, Area, or Project", placeholder="Start typing...")
    
    # Filter Data
    filtered = df.copy()
    if search:
        mask = filtered.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)
        filtered = filtered[mask]

    # Display results
    st.write(f"Showing {len(filtered)} results")
    
    for _, row in filtered.iterrows():
        # Try to find the link column
        link_col = [c for c in df.columns if 'Agent Pack' in c or 'Link' in c]
        link = row[link_col[0]] if link_col and pd.notnull(row[link_col[0]]) else None

        with st.container():
            st.markdown(f"""
            <div class="project-card">
                <h2 style="margin:0; color: #1E3A8A;">{row.get('Project Name', 'Unnamed Project')}</h2>
                <p style="font-size: 1.1em;"><b>{row.get('Developer', 'N/A')}</b> | {row.get('Community/Area', 'N/A')}</p>
                <p>📅 <b>Handover:</b> {row.get('Handover Date', 'TBC')}</p>
                {"<a href='" + str(link) + "' target='_blank' class='link-btn'>📂 Open Agent Pack (Drive)</a>" if link and str(link).startswith('http') else "<i style='color:gray;'>No link available</i>"}
            </div>
            """, unsafe_allow_html=True)
else:
    st.error("⚠️ Error: 'data.csv' not found or file format is incorrect. Please ensure you renamed your CSV to 'data.csv' on GitHub.")
