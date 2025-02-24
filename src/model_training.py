from sklearn.linear_model import LinearRegression
import numpy as np
import json
import os
import joblib

def train_model(game_id):
    """gameId'ye göre modeli eğitir."""
    filename = f"../data/{game_id}_data.json"
    if not os.path.exists(filename):
        print(f"{game_id} için yeterli veri yok.")
        return

    with open(filename, "r") as file:
        data = json.load(file)

    # Verileri modele uygun hale getir
    X = []
    y = []
    for entry in data:
        if "coefficient" in entry.get("arguments", [{}])[0]:
            X.append([entry["arguments"][0]["second"]])  # Özellik: second
            y.append(entry["arguments"][0]["coefficient"])  # Hedef: coefficient

    if not X:
        print(f"{game_id} için eğitim verisi bulunamadı.")
        return

    # Modeli eğit
    model = LinearRegression()
    model.fit(X, y)
    print(f"{game_id} için model eğitildi.")

    # Modeli kaydet
    os.makedirs("../models", exist_ok=True)  # models klasörü yoksa oluştur
    joblib.dump(model, f"../models/{game_id}_model.pkl")