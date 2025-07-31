import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from utils import top3_preprocessing

def render():
    st.header("📈 Analisis Pola Angka 4D")

    df = st.session_state.get("data_df", None)
    if df is None or len(df) < 10:
        st.warning("Data terlalu sedikit. Minimal 10 baris.")
        return

    digit_df = top3_preprocessing.split_digits(df)

    st.subheader("🔢 Frekuensi Digit per Posisi")
    freq_df = pd.DataFrame()
    for pos in digit_df:
        freq = digit_df[pos].value_counts().sort_index()
        freq_df[pos] = freq
    st.dataframe(freq_df.fillna(0).astype(int).T)

    st.subheader("📊 Heatmap Frekuensi")
    fig, ax = plt.subplots()
    sns.heatmap(freq_df.fillna(0).astype(int).T, cmap="YlGnBu", annot=True, fmt='g', ax=ax)
    st.pyplot(fig)

    st.subheader("⏱️ Delay Kemunculan Digit")
    delay_info = {}
    for pos in digit_df:
        last_seen = {}
        delays = []
        for i, d in enumerate(digit_df[pos]):
            if d in last_seen:
                delays.append(i - last_seen[d])
            last_seen[d] = i
        delay_info[pos] = sum(delays)/len(delays) if delays else 0
    st.json(delay_info)

    st.subheader("📉 Tren Naik/Turun Digit")
    trend_df = pd.DataFrame()
    for pos in digit_df:
        trend_df[pos] = digit_df[pos].astype(int).diff()
    st.line_chart(trend_df)

    st.markdown("---")
    st.markdown("✅ Analisis ini membantu menyesuaikan model dan mengenali pola berulang dari masa lalu.")
