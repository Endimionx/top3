import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import LSTM, Dense
from sklearn.preprocessing import OneHotEncoder
import joblib
import os

def build_lstm_model(input_shape, output_dim=10):
    model = Sequential()
    model.add(LSTM(64, input_shape=input_shape))
    model.add(Dense(output_dim, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

def prepare_data(series, window_size=10):
    X, y = [], []
    for i in range(len(series) - window_size):
        seq_x = series[i:i+window_size]
        seq_y = series[i+window_size]
        X.append(seq_x)
        y.append(seq_y)
    return np.array(X), np.array(y)

def train_lstm(df, posisi, window_size=10, save_dir="models"):
    series = df["angka_4d"].astype(str).str.zfill(4).apply(lambda x: x["ribuan ratusan puluhan satuan".split().index(posisi)])
    encoder = OneHotEncoder(sparse_output=False, categories=[list("0123456789")])
    X, y = prepare_data(series.tolist(), window_size)
    X_enc = encoder.fit_transform(X)
    y_enc = encoder.fit_transform(y.reshape(-1, 1))
    X_enc = X_enc.reshape((X_enc.shape[0], window_size, 10))

    model = build_lstm_model((window_size, 10))
    model.fit(X_enc, y_enc, epochs=50, batch_size=16, verbose=0)

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    model.save(f"{save_dir}/lstm_{posisi}.h5")
    joblib.dump(encoder, f"{save_dir}/encoder_{posisi}.pkl")
    return model

def predict_top6(df, posisi, window_size=10, save_dir="models"):
    from keras.models import load_model

    model_path = f"{save_dir}/lstm_{posisi}.h5"
    encoder_path = f"{save_dir}/encoder_{posisi}.pkl"

    if not os.path.exists(model_path) or not os.path.exists(encoder_path):
        raise FileNotFoundError(f"Model {posisi} belum dilatih.")

    model = load_model(model_path)
    encoder = joblib.load(encoder_path)

    series = df["angka_4d"].astype(str).str.zfill(4).apply(lambda x: x["ribuan ratusan puluhan satuan".split().index(posisi)])
    seq = series[-window_size:].tolist()
    seq_enc = encoder.transform([seq])
    seq_enc = seq_enc.reshape((1, window_size, 10))

    pred = model.predict(seq_enc)[0]
    top6 = np.argsort(pred)[-6:][::-1]
    return [str(i) for i in top6]
