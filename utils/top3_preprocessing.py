import pandas as pd

def split_digits(df):
    """
    Memecah angka_4d menjadi kolom digit per posisi:
    - ribuan, ratusan, puluhan, satuan
    """
    digits = {"ribuan": [], "ratusan": [], "puluhan": [], "satuan": []}
    for angka in df["angka_4d"]:
        angka = str(angka).zfill(4)
        digits["ribuan"].append(angka[0])
        digits["ratusan"].append(angka[1])
        digits["puluhan"].append(angka[2])
        digits["satuan"].append(angka[3])
    return {k: pd.Series(v) for k, v in digits.items()}

def combine_top6(top6_dict):
    """
    Menggabungkan semua kombinasi top-6 dari tiap posisi menjadi angka 4D.
    """
    from itertools import product
    rib, rat, pul, sat = top6_dict["ribuan"], top6_dict["ratusan"], top6_dict["puluhan"], top6_dict["satuan"]
    result = ["".join(p) for p in product(rib, rat, pul, sat)]
    return result

def normalize_confidence(score_dict):
    """
    Normalisasi confidence agar distribusi lebih seimbang.
    """
    import numpy as np
    norm_scores = {}
    for pos in score_dict:
        arr = np.array(score_dict[pos])
        if arr.max() - arr.min() == 0:
            norm = [1.0]*len(arr)
        else:
            norm = ((arr - arr.min()) / (arr.max() - arr.min())).tolist()
        norm_scores[pos] = norm
    return norm_scores
