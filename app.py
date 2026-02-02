import streamlit as st
import pandas as pd

st.set_page_config(page_title="UHRE Master Portal", layout="wide")

@st.cache_data
def load_data():
    # We are now looking for the .xlsx file you just uploaded
    file_path = 'data.xlsx' 
    try:
        # Excel files handle the "GetURL" links much better than CSVs
        df = pd.read_excel(file_path, engine='openpyxl')
        
        # Clean the column names
        df.columns = [str(c).replace('\n', ' ').strip() for c in df.columns]
        return df
    except Exception as e:
        st.error(f"Could not find or read {file_path}. Error: {e}")
        return None

df = load_data()

# ... (the rest of your display code from before)
