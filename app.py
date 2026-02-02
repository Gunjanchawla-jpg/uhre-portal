import streamlit as st
import pandas as pd

st.set_page_config(page_title="UHRE Agent Portal", layout="wide")

# Custom CSS for a professional look
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
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    # Fixes the 'utf-8' and 'cp1252' errors automatically
    try:
        df = pd.read_csv('data.csv', encoding='utf-8')
    except:
        df = pd.read_csv('data.csv', encoding='cp1252')
    
    # Clean the column names so they are easy to work with
    df.columns = df.columns.str.replace(r'\n', ' ', regex=True).str.strip()
    return df

df = load_data()

st.title("🏙️ UHRE Master Project Database")

if df is not None:
    # Search box for agents
    search = st.text_input("🔍 Search by Developer, Area, or Project", placeholder="e.g. Emaar, Dubailand...")
    
    # Filtering
    filtered = df.copy()
    if search:
        mask = filtered.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)
        filtered = filtered[mask]

    # Show results as cards
    for _, row in filtered.iterrows():
        # Identify the link column even if the name is slightly different
        link_col = [c for c in df.columns if 'Agent Pack' in c or 'Link' in c]
        link = row[link_col[0]] if link_col and pd.notnull(row[link_col[0]]) else None

        with st.container():
            st.markdown(f"""
            <div class="project-card">
                <h2 style="margin:0;">{row.get('Project Name', 'Unnamed Project')}</h2>
                <p style="color:#666;"><b>{row.get('Developer', 'N/A')}</b> | {row.get('Community/Area', 'N/A')}</p>
                <p>📅 Handover: {row.get('Handover Date', 'TBC')}</p>
                {"<a href='" + str(link) + "' target='_blank' class='link-btn'>📂 Open Agent Pack</a>" if link and str(link).startswith('http') else "<i style='color:gray;'>No link available yet</i>"}
            </div>
            """, unsafe_allow_html=True)
else:
    st.error("Could not load data. Please check if 'data.csv' exists on GitHub.")
