import streamlit as st
import pandas as pd
from utils import top3_preprocessing, top3_ensemble
from models import top3_lstm_model, top3_transformer_model
from top3_markov_hybrid import top6_markov_hybrid
from top3_markov_predictor import predict_markov_order1_single

def simulate_real_prediction(df):
    real = df.iloc[-1]["angka_4d"]
    digit_dfs = top3_preprocessing.split_digits(df[:-1])

    results = {}
    correct = {}
    for pos in ["ribuan", "ratusan", "puluhan", "satuan"]:
        lstm = top3_lstm_model.predict_top6(digit_dfs[pos])
        trans = top3_transformer_model.predict_top6(digit_dfs[pos])
        markov = top3_markov_model.top6_markov_hybrid(digit_dfs[pos])
        final, _ = top3_ensemble.auto_hybrid_ensemble(lstm, trans, markov, pos)
        results[pos] = final
        correct[pos] = int(real["0123".index(pos[0])] in final)

    return results, real, correct

def render():
    st.header("📊 Simulasi & Evaluasi Prediksi")

    df = st.session_state.get("data_df", None)
    if df is None or len(df) < 20:
        st.warning("Data terlalu sedikit. Minimal 20 baris untuk simulasi.")
        return

    st.markdown("### 🎯 Simulasi Terhadap Data Terakhir")
    results, real, correct = simulate_real_prediction(df)

    sim_data = {
        "Posisi": ["Ribuan", "Ratusan", "Puluhan", "Satuan"],
        "Top-6 Prediksi": [", ".join(results[p]) for p in results],
        "Target Real": list(real),
        "Tepat?": ["✅" if correct[p] else "❌" for p in results]
    }
    st.table(pd.DataFrame(sim_data))

    acc = sum(correct.values()) / 4
    st.success(f"🎯 Akurasi Simulasi (Top-6): `{acc*100:.2f}%`")

    if "prediction_log" not in st.session_state:
        st.session_state.prediction_log = []
    st.session_state.prediction_log.append({"real": real, "pred": results, "acc": acc})

    st.markdown("---")
    st.markdown("### 📁 Riwayat Simulasi")
    if len(st.session_state.prediction_log) > 0:
        logs = st.session_state.prediction_log
        log_df = pd.DataFrame([{
            "Target": l["real"],
            "Akurasi": f"{l['acc']*100:.2f}%"
        } for l in logs])
        st.dataframe(log_df, use_container_width=True)

    if st.button("🗑️ Hapus Riwayat"):
        st.session_state.prediction_log = []
        st.success("Riwayat simulasi dihapus.")
