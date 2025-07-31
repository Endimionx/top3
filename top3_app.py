import streamlit as st
from tabs import top3_tab1_input, top3_tab2_prediction, top3_tab3_simulation, top3_tab4_pattern_analysis

st.set_page_config(page_title="Prediktor 4D Canggih", layout="wide")

# Inisialisasi session state global
if 'data_df' not in st.session_state:
    st.session_state.data_df = None
if 'lokasi_prediksi' not in st.session_state:
    st.session_state.lokasi_prediksi = "global"
if 'prediction_log' not in st.session_state:
    st.session_state.prediction_log = []

# Navigasi tab
tabs = ["Input Data", "Prediksi Angka 4D", "Simulasi & Evaluasi", "Analisis Pola"]
selected_tab = st.sidebar.radio("Navigasi", tabs)

if selected_tab == "Input Data":
    top3_tab1_input.render()
elif selected_tab == "Prediksi Angka 4D":
    top3_tab2_prediction.render()
elif selected_tab == "Simulasi & Evaluasi":
    top3_tab3_simulation.render()
elif selected_tab == "Analisis Pola":
    top3_tab4_pattern_analysis.render()
