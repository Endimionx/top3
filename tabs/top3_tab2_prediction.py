import streamlit as st
from utils import top3_preprocessing, top3_ensemble
from models import top3_lstm_model, top3_transformer_model
from top3_markov_predictor import top6_markov, top6_markov_order2

import pandas as pd

def render():
    st.header("🎯 Prediksi Angka 4D")

    df = st.session_state.get("data_df", None)
    if df is None:
        st.warning("Silakan input data terlebih dahulu di Tab 1.")
        return

    digit_dfs = top3_preprocessing.split_digits(df)

    st.markdown("### ✅ Prediksi Per Posisi (0-9)")
    results = {}

    for pos in ["ribuan", "ratusan", "puluhan", "satuan"]:
        st.subheader(f"📌 Posisi: {pos.capitalize()}")

        lstm_top6 = top3_lstm_model.predict_top6(digit_dfs[pos])
        transformer_top6 = top3_transformer_model.predict_top6(digit_dfs[pos])
        markov_top6 = top3_markov_model.top6_markov_hybrid(digit_dfs[pos])

        final_top6, detail = top3_ensemble.auto_hybrid_ensemble(
            lstm_top6, transformer_top6, markov_top6, pos
        )
        results[pos] = final_top6

        st.write(f"Top-6 Prediksi: `{final_top6}`")
        with st.expander("🔍 Rincian Hybrid Voting"):
            st.json(detail)

    # Gabungkan kombinasi akhir
    st.markdown("---")
    st.subheader("🎲 Kombinasi Final Prediksi 4D")
    prediksi_4d = top3_preprocessing.generate_combinations(results)
    st.write(prediksi_4d)

    # Simpan ke session
    st.session_state["prediksi_top6"] = results
    st.session_state["prediksi_kombinasi_4d"] = prediksi_4d
