from collections import Counter
import numpy as np

def ensemble_top6(*args):
    """
    Gabungkan semua list top6 menjadi satu ensemble berdasarkan frekuensi kemunculan.
    args: list of list, misalnya [top6_conf, top6_prob, top6_lstm, top6_markov]
    """
    counter = Counter()
    for lst in args:
        for i, val in enumerate(lst):
            counter[val] += (6 - i)  # beri bobot pada ranking
    sorted_items = counter.most_common(6)
    return [item[0] for item in sorted_items]

def hybrid_voting(top6_conf, top6_prob, alpha=0.5):
    """
    Voting gabungan confidence dan probabilistic berdasarkan bobot alpha.
    """
    counter = Counter()
    for i, val in enumerate(top6_conf):
        counter[val] += (6 - i) * alpha
    for i, val in enumerate(top6_prob):
        counter[val] += (6 - i) * (1 - alpha)
    sorted_items = counter.most_common(6)
    return [item[0] for item in sorted_items]

def stacked_hybrid(conf, prob, lstm, markov):
    """
    Final ensemble stacked hybrid: confidence + prob + lstm + markov
    """
    return ensemble_top6(conf, prob, lstm, markov)

def meta_voting(conf, prob, hybrid, acc_conf, acc_prob, acc_hybrid):
    """
    Pilih metode terbaik berdasarkan akurasi terakhir (meta learning sederhana).
    """
    scores = {"conf": acc_conf, "prob": acc_prob, "hybrid": acc_hybrid}
    best = max(scores, key=scores.get)
    if best == "conf":
        return conf
    elif best == "prob":
        return prob
    else:
        return hybrid
