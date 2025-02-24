import os
import json

def save_data(data, game_id):
    """Gelen verileri gameId'ye göre kaydeder."""
    filename = f"../data/{game_id}_data.json"
    os.makedirs("../data", exist_ok=True)  # data klasörü yoksa oluştur

    # Eğer dosya varsa, mevcut verileri oku ve yeni veriyi ekle
    if os.path.exists(filename):
        with open(filename, "r") as file:
            existing_data = json.load(file)
    else:
        existing_data = []

    existing_data.append(data)  # Yeni veriyi ekle

    # Verileri dosyaya yaz
    with open(filename, "w") as file:
        json.dump(existing_data, file, indent=4)