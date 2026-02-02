import streamlit as st
import pandas as pd
from io import BytesIO

# 1. UI Configuration - Makes it look like a professional App
st.set_page_config(page_title="UHRE Agent Hub", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #F4F7F9; }
    .project-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 6px solid #004AAD;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 1rem;
    }
    .status-badge {
        background-color: #E0E7FF;
        color: #4338CA;
        padding: 2px 10px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Data Loading
@st.cache_data
def get_data():
    df = pd.read_csv('UHRE_All_Tabs_Merged (1).xlsx - Merged.csv')
    df.columns = df.columns.str.strip() # Clean column names
    return df

try:
    df = get_data()

    # 3. Sidebar Filters
    st.sidebar.title("🏢 UHRE Filter")
    search = st.sidebar.text_input("🔍 Quick Search", placeholder="Project or Developer...")
    
    dev_list = ["All"] + sorted(df['Developer'].dropna().unique().tolist())
    selected_dev = st.sidebar.selectbox("Developer", dev_list)

    area_list = ["All"] + sorted(df['Community/Area'].dropna().unique().tolist())
    selected_area = st.sidebar.selectbox("Community/Area", area_list)

    # Filtering Logic
    filtered = df.copy()
    if search:
        filtered = filtered[filtered.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)]
    if selected_dev != "All":
        filtered = filtered[filtered['Developer'] == selected_dev]
    if selected_area != "All":
        filtered = filtered[filtered['Community/Area'] == selected_area]

    # 4. Top Header & Download
    col_t1, col_t2 = st.columns([3, 1])
    with col_t1:
        st.title("Project Inventory Portal")
        st.write(f"Showing **{len(filtered)}** active projects")
    
    with col_t2:
        # Excel Export
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            filtered.to_excel(writer, index=False)
        st.download_button("📥 Export Selected", output.getvalue(), "UHRE_Report.xlsx", use_container_width=True)

    st.divider()

    # 5. UI Appealing "Card" View for Agents
    # This loop turns every row of your Excel into a mobile-friendly card
    for _, row in filtered.iterrows():
        with st.container():
            st.markdown(f"""
            <div class="project-card">
                <div style="display: flex; justify-content: space-between;">
                    <h2 style="margin:0; color:#1E293B;">{row['Project Name']}</h2>
                    <span class="status-badge">{row['Developer']}</span>
                </div>
                <p style="color:#64748B; margin: 5px 0;">📍 {row['Community/Area']}</p>
                <div style="margin-top:10px;">
                    <b>📅 Launch:</b> {row['Launch Date']} | <b>🔑 Handover:</b> {row['Handover Date']}
                </div>
                <div style="margin-top:15px;">
                    <a href="{row['Agent Pack \n  (Google Drive)']}" target="_blank" 
                       style="background-color:#004AAD; color:white; padding:8px 15px; border-radius:5px; text-decoration:none; font-size:14px;">
                       📂 Open Marketing Assets
                    </a>
                </div>
            </div>
            """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"Please ensure the CSV file is in the folder. Error: {e}")