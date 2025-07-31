import pandas as pd
from collections import defaultdict, Counter

def top6_markov(df, posisi='ribu'):
    """
    Markov Order-1 untuk prediksi digit posisi tertentu.
    """
    data = df[posisi].astype(str).tolist()
    transitions = defaultdict(list)

    for i in range(len(data) - 1):
        transitions[data[i]].append(data[i + 1])

    probs = {k: Counter(v) for k, v in transitions.items()}
    last = data[-1]

    if last in probs:
        prediksi = probs[last].most_common(6)
    else:
        prediksi = Counter(data).most_common(6)
    
    return [int(p[0]) for p in prediksi]

def top6_markov_order2(df, posisi='ribu'):
    """
    Markov Order-2: melihat dua digit sebelumnya.
    """
    data = df[posisi].astype(str).tolist()
    transitions = defaultdict(list)

    for i in range(len(data) - 2):
        key = data[i] + data[i+1]
        transitions[key].append(data[i+2])

    key = data[-2] + data[-1]
    probs = transitions.get(key, [])

    if probs:
        return [int(x) for x, _ in Counter(probs).most_common(6)]
    else:
        return Counter(data).most_common(6)

def top6_markov_hybrid(df):
    """
    Hybrid Markov (gabungan order-1 dan order-2) untuk semua posisi.
    """
    hasil = {}
    for posisi in ['ribu', 'ratu', 'pulu', 'satu']:
        top1 = top6_markov(df, posisi)
        top2 = top6_markov_order2(df, posisi)
        gabung = Counter(top1 + top2).most_common(6)
        hasil[posisi] = [x for x, _ in gabung]
    return hasil
