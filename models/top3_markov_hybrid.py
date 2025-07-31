# top3_markov_hybrid.py
import pandas as pd
from collections import Counter

def top6_markov(df, pos):
    transitions = {}
    for i in range(len(df) - 1):
        prev = str(df.iloc[i][pos])
        curr = str(df.iloc[i + 1][pos])
        if prev not in transitions:
            transitions[prev] = []
        transitions[prev].append(curr)

    last = str(df.iloc[-1][pos])
    next_digits = transitions.get(last, [])
    counter = Counter(next_digits)
    top6 = [int(x[0]) for x in counter.most_common(6)]
    while len(top6) < 6:
        for d in range(10):
            if d not in top6:
                top6.append(d)
            if len(top6) == 6:
                break
    return top6

def top6_markov_order2(df, pos):
    transitions = {}
    for i in range(len(df) - 2):
        prev2 = str(df.iloc[i][pos]) + str(df.iloc[i + 1][pos])
        curr = str(df.iloc[i + 2][pos])
        if prev2 not in transitions:
            transitions[prev2] = []
        transitions[prev2].append(curr)

    last2 = str(df.iloc[-2][pos]) + str(df.iloc[-1][pos])
    next_digits = transitions.get(last2, [])
    counter = Counter(next_digits)
    top6 = [int(x[0]) for x in counter.most_common(6)]
    while len(top6) < 6:
        for d in range(10):
            if d not in top6:
                top6.append(d)
            if len(top6) == 6:
                break
    return top6

def top6_markov_hybrid(df, pos):
    result1 = top6_markov(df, pos)
    result2 = top6_markov_order2(df, pos)
    combined = result1 + result2
    counter = Counter(combined)
    top6 = [int(x[0]) for x in counter.most_common(6)]
    while len(top6) < 6:
        for d in range(10):
            if d not in top6:
                top6.append(d)
            if len(top6) == 6:
                break
    return top6
