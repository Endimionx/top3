def meta_select_best(conf, prob, hybrid, acc_conf, acc_prob, acc_hybrid):
    """
    Pilih hasil voting terbaik berdasarkan akurasi historis.
    Bisa dikembangkan dengan model pembelajaran (meta-learning).
    """
    skor = {
        "conf": acc_conf,
        "prob": acc_prob,
        "hybrid": acc_hybrid
    }

    terbaik = max(skor, key=skor.get)

    if terbaik == "conf":
        return conf
    elif terbaik == "prob":
        return prob
    else:
        return hybrid

def auto_ensemble_adaptive(conf, prob, hybrid, markov, acc_dict, alpha=0.5):
    """
    Gabungan dari semua metode: hybrid + markov + adaptive alpha.
    """
    hasil = {}
    for posisi in ['ribu', 'ratu', 'pulu', 'satu']:
        # Ambil top6 dari semua metode
        hybrid6 = hybrid.get(posisi, [])
        markov6 = markov.get(posisi, [])
        conf6 = conf.get(posisi, [])
        prob6 = prob.get(posisi, [])

        # Gabungkan dengan bobot adaptif
        gabung = hybrid6 + markov6 + conf6 + prob6
        counter = {}
        for d in gabung:
            counter[d] = counter.get(d, 0) + 1

        sorted_top = sorted(counter.items(), key=lambda x: -x[1])
        hasil[posisi] = [x[0] for x in sorted_top[:6]]
    return hasil
