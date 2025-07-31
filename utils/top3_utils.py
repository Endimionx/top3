import numpy as np
import pandas as pd

def top3_ensemble(confidence_dict, probabilistic_dict, stacked_dict=None, markov_dict=None, alpha=0.5):
    """
    Menggabungkan hasil prediksi dari beberapa sumber:
    - confidence_dict: hasil voting confidence
    - probabilistic_dict: hasil probabilistic voting
    - stacked_dict: hasil hybrid stacking
    - markov_dict: hasil dari markov hybrid
    Output: dict berisi top-6 digit prediksi per posisi
    """

    positions = ['ribuan', 'ratusan', 'puluhan', 'satuan']
    result = {}

    for pos in positions:
        # Voting score awal
        score = {}

        # Confidence voting
        for i, digit in enumerate(confidence_dict.get(pos, [])):
            score[digit] = score.get(digit, 0) + (6 - i) * alpha

        # Probabilistic voting
        for i, digit in enumerate(probabilistic_dict.get(pos, [])):
            score[digit] = score.get(digit, 0) + (6 - i) * (1 - alpha)

        # Tambahan dari stacked hybrid jika ada
        if stacked_dict and pos in stacked_dict:
            for i, digit in enumerate(stacked_dict[pos]):
                score[digit] = score.get(digit, 0) + (6 - i) * 0.3  # bobot tambahan

        # Tambahan dari markov hybrid jika ada
        if markov_dict and pos in markov_dict:
            for i, digit in enumerate(markov_dict[pos]):
                score[digit] = score.get(digit, 0) + (6 - i) * 0.2  # bobot tambahan

        # Ambil top-6 berdasarkan skor total
        sorted_digits = sorted(score.items(), key=lambda x: x[1], reverse=True)
        result[pos] = [digit for digit, _ in sorted_digits[:6]]

    return result
