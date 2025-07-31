import numpy as np
import pandas as pd

def autotune_alpha(acc_conf, acc_prob):
    """
    Otomatis memilih alpha terbaik berdasarkan akurasi confidence dan probabilistic.
    """
    total = acc_conf + acc_prob + 1e-6
    alpha = acc_conf / total
    return round(alpha, 2)

def pilih_ws_stabil(df_ws_result, top_n=3):
    """
    Memilih WS terbaik berdasarkan stabilitas (akurasi - std dev).
    """
    df_ws_result["stability"] = df_ws_result["accuracy"] - df_ws_result["std"]
    return df_ws_result.sort_values(by="stability", ascending=False).head(top_n)

def detect_ws_gagal(log_df, posisi, threshold=0.2):
    """
    Mendeteksi WS yang sering gagal untuk posisi tertentu.
    """
    failed = log_df[log_df["status"] == "miss"]
    counts = failed[failed["posisi"] == posisi]["ws"].value_counts()
    return counts[counts >= threshold * len(failed)]

def normalize_confidence(scores):
    """
    Normalisasi confidence agar lebih seimbang.
    """
    scores = np.array(scores)
    if scores.max() == scores.min():
        return [1 / len(scores)] * len(scores)
    return list((scores - scores.min()) / (scores.max() - scores.min()))
