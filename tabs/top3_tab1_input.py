import streamlit as st
import pandas as pd

def render():
    st.header("📝 Input Data Angka 4D")
    
    uploaded_file = st.file_uploader("Upload file CSV (format 4 digit, satu kolom)", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        if df.shape[1] != 1:
            st.error("File harus memiliki 1 kolom saja (angka 4D per baris).")
            return
        df.columns = ["angka_4d"]
        st.session_state.data_df = df
        st.success(f"Berhasil memuat {len(df)} data.")

    st.markdown("### Atau input manual:")
    input_text = st.text_area("Masukkan angka 4D (dipisah baris)", height=150)
    if st.button("Simpan Manual"):
        lines = input_text.strip().split("\n")
        cleaned = [x.strip() for x in lines if x.strip().isdigit() and len(x.strip()) == 4]
        if len(cleaned) == 0:
            st.warning("Tidak ada angka valid yang dimasukkan.")
            return
        df = pd.DataFrame(cleaned, columns=["angka_4d"])
        st.session_state.data_df = df
        st.success(f"Berhasil menyimpan {len(df)} data manual.")

    if st.session_state.data_df is not None:
        st.markdown("### Contoh Data:")
        st.dataframe(st.session_state.data_df.tail(10), use_container_width=True)
