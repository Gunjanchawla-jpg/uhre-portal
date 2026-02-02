@st.cache_data
def load_data():
    # List of encodings to try in order of likelihood
    encodings = ['utf-8', 'cp1252', 'latin1', 'utf-16']
    
    for enc in encodings:
        try:
            # Added 'on_bad_lines' and 'encoding_errors' to prevent crashes
            df = pd.read_csv('data.csv', encoding=enc, on_bad_lines='skip', encoding_errors='ignore')
            
            # Clean column names
            df.columns = df.columns.str.replace(r'\n', ' ', regex=True).str.strip()
            return df
        except Exception:
            continue
            
    st.error("❌ All encoding attempts failed. Please resave your file as 'CSV UTF-8'.")
    return None
