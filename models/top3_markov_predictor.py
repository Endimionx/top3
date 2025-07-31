# top3_markov_predictor.py
from collections import defaultdict, Counter
import pandas as pd

def predict_markov_order1_single(df, pos):
    transitions = defaultdict(list)
    for i in range(len(df) - 1):
        prev = str(df.iloc[i][pos])
        curr = str(df.iloc[i + 1][pos])
        transitions[prev].append(curr)
    last = str(df.iloc[-1][pos])
    counter = Counter(transitions.get(last, []))
    top6 = [int(x[0]) for x in counter.most_common(6)]
    while len(top6) < 6:
        for d in range(10):
            if d not in top6:
                top6.append(d)
            if len(top6) == 6:
                break
    return top6

def predict_markov_order2_single(df, pos):
    transitions = defaultdict(list)
    for i in range(len(df) - 2):
        prev = str(df.iloc[i][pos]) + str(df.iloc[i + 1][pos])
        curr = str(df.iloc[i + 2][pos])
        transitions[prev].append(curr)
    last = str(df.iloc[-2][pos]) + str(df.iloc[-1][pos])
    counter = Counter(transitions.get(last, []))
    top6 = [int(x[0]) for x in counter.most_common(6)]
    while len(top6) < 6:
        for d in range(10):
            if d not in top6:
                top6.append(d)
            if len(top6) == 6:
                break
    return top6
