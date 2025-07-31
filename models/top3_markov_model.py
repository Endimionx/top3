import pandas as pd
from collections import defaultdict, Counter

def get_transitions(series, order=1):
    transitions = defaultdict(Counter)
    for i in range(len(series) - order):
        prev = tuple(series[i:i+order])
        next_val = series[i+order]
        transitions[prev][next_val] += 1
    return transitions

def predict_markov(transitions, prev_seq, top_k=6):
    counter = transitions.get(tuple(prev_seq), Counter())
    most_common = counter.most_common(top_k)
    return [item[0] for item in most_common]

def top6_markov(df, posisi):
    series = df["angka_4d"].astype(str).str.zfill(4).apply(lambda x: x["ribuan ratusan puluhan satuan".split().index(posisi)])
    transitions = get_transitions(series.tolist(), order=1)
    prev_seq = series.iloc[-1:]
    return predict_markov(transitions, prev_seq.tolist(), top_k=6)

def top6_markov_order2(df, posisi):
    series = df["angka_4d"].astype(str).str.zfill(4).apply(lambda x: x["ribuan ratusan puluhan satuan".split().index(posisi)])
    transitions = get_transitions(series.tolist(), order=2)
    prev_seq = series.iloc[-2:]
    return predict_markov(transitions, prev_seq.tolist(), top_k=6)

def top6_markov_hybrid(df, posisi):
    try:
        top1 = top6_markov(df, posisi)
        top2 = top6_markov_order2(df, posisi)
        combined = list(dict.fromkeys(top2 + top1))  # preserve order, remove duplicates
        return combined[:6]
    except Exception:
        return ['0', '1', '2', '3', '4', '5']
