import json
import os
import msvcrt  # Windows için klavye girişi modülü

def load_games():
    """Oyunları config dosyasından yükler."""
    with open('config/games.json', 'r') as file:
        config = json.load(file)
        return config['games']

def select_game():
    """Kullanıcının oyun seçmesini sağlar."""
    games = load_games()
    selected_index = 0

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')  # Ekranı temizle
        print("Lütfen bir oyun seçin (Yukarı/Aşağı tuşlarıyla seçin, Enter ile onaylayın):\n")
        
        for i, game in enumerate(games):
            prefix = ">" if i == selected_index else " "
            print(f"{prefix} {game['name']} ({game['gameId']})")

        key = msvcrt.getch()  # Kullanıcı girişini al
        if key == b'\xe0':  # Özel tuşlar (yukarı/aşağı) için
            key = msvcrt.getch()
            if key == b'H':  # Yukarı tuşu
                selected_index = max(0, selected_index - 1)
            elif key == b'P':  # Aşağı tuşu
                selected_index = min(len(games) - 1, selected_index + 1)
        elif key == b'\r':  # Enter tuşu
            return games[selected_index]  # Seçilen oyunu döndür