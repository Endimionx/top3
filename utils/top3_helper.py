import numpy as np
import pandas as pd

def normalize_scores(scores):
    """
    Normalisasi nilai (confidence/probabilitas) ke skala 0-1.
    """
    scores = np.array(scores, dtype=np.float32)
    if np.max(scores) == np.min(scores):
        return [1/len(scores)] * len(scores)
    norm = (scores - np.min(scores)) / (np.max(scores) - np.min(scores))
    return norm.tolist()

def evaluate_top6(pred_list, target):
    """
    Evaluasi apakah target termasuk dalam prediksi top-6.
    """
    return int(target in pred_list)

def convert_to_digits(df_angka):
    """
    Ubah kolom 'angka' menjadi digit: ribu, ratu, pulu, satu.
    """
    df = df_angka.copy()
    df['angka'] = df['angka'].astype(str).str.zfill(4)
    df['ribu'] = df['angka'].str[0].astype(int)
    df['ratu'] = df['angka'].str[1].astype(int)
    df['pulu'] = df['angka'].str[2].astype(int)
    df['satu'] = df['angka'].str[3].astype(int)
    return df[['ribu', 'ratu', 'pulu', 'satu']]

def top6_accuracy_score(all_preds, targets):
    """
    Hitung akurasi top-6 per posisi digit.
    """
    score = {}
    for pos in ['ribu', 'ratu', 'pulu', 'satu']:
        acc = np.mean([evaluate_top6(preds, tgt) for preds, tgt in zip(all_preds[pos], targets[pos])])
        score[pos] = round(acc, 4)
    return score

def digit_stat(df_digit):
    """
    Statistik ganjil/genap, besar/kecil per posisi.
    """
    stat = {}
    for pos in ['ribu', 'ratu', 'pulu', 'satu']:
        d = df_digit[pos]
        stat[pos] = {
            "ganjil": int((d % 2 == 1).sum()),
            "genap": int((d % 2 == 0).sum()),
            "besar": int((d >= 5).sum()),
            "kecil": int((d < 5).sum()),
        }
    return stat
