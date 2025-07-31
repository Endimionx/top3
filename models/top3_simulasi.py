import pandas as pd

def simulate_real_prediction(df, hasil_prediksi_dict):
    """
    Simulasikan hasil prediksi terhadap angka real terakhir di df.
    - df: DataFrame berisi data 4D historis
    - hasil_prediksi_dict: dict hasil prediksi per posisi: {'ribu': [...], 'ratu': [...], ...}
    """
    target = df.iloc[-1]
    result = {}
    status = []

    for posisi in ['ribu', 'ratu', 'pulu', 'satu']:
        prediksi = hasil_prediksi_dict.get(posisi, [])
        target_digit = int(str(target)[-4:][['ribu', 'ratu', 'pulu', 'satu'].index(posisi)])
        tepat = target_digit in prediksi
        result[posisi] = {
            "target": target_digit,
            "prediksi": prediksi,
            "status": "✔️" if tepat else "❌"
        }
        status.append(tepat)

    total_tepat = sum(status)
    status_akhir = f"{total_tepat}/4 Posisi Tepat"
    return result, status_akhir

def log_prediksi(log_df, tanggal, prediksi, real, status):
    """
    Tambahkan satu entri ke log DataFrame.
    """
    new_row = {
        "tanggal": tanggal,
        "prediksi": prediksi,
        "real": real,
        "status": status
    }
    return pd.concat([log_df, pd.DataFrame([new_row])], ignore_index=True)

def evaluasi_log(log_df):
    """
    Evaluasi akurasi berdasarkan log prediksi.
    """
    if len(log_df) == 0:
        return "Belum ada data."
    
    benar = log_df["status"].apply(lambda x: "4" in x).sum()
    total = len(log_df)
    return f"Akurasi {benar}/{total} prediksi tepat semua digit ({round(100*benar/total, 2)}%)"
