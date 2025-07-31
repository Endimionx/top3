# top3 - Aplikasi Prediksi Angka 4D Akurat

`top3` adalah aplikasi berbasis Streamlit untuk prediksi angka 4D, didukung oleh metode modern: LSTM, Markov, Hybrid Voting, dan Analisis Pola Historis. Sistem ini didesain agar tajam dan adaptif terhadap pola data terbaru.

## 🔧 Fitur Utama

### Tab1: Data dan Input
- Input manual atau unggah file
- Format angka 4D (contoh: 1234)
- Visualisasi data terakhir

### Tab2: Manajemen Model
- Latih model per posisi digit: ribuan, ratusan, puluhan, satuan
- Atur Window Size (WS), metode, dan epoch
- Load dan simpan model otomatis

### Tab3: Prediksi & Ensemble
- Prediksi top-6 digit per posisi
- Voting: Confidence, Probabilistic, Hybrid, Stacked Hybrid
- Auto-tuning Alpha (berbasis akurasi)
- Simulasi Live Accuracy
- Logging otomatis hasil prediksi
- Auto Ensemble Adaptive

### Tab4: Analisis Pola
- Statistik digit dan kombinasi
- Delay kemunculan, tren naik/turun
- Heatmap posisi digit
- Rule-based pattern: zigzag, mirror, kembar, selisih tetap, dll
- Deteksi pola historis dan kelanjutan

## 📁 Struktur Folder
