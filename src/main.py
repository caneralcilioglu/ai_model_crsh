import sys
import os

# Proje kök dizinini Python'un modül yoluna ekle
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game_selection import select_game
from websocket_client import connect_socket
import threading

def main():
    # Oyun seçme işlemi
    selected_game = select_game()
    print(f"Seçilen Oyun: {selected_game['name']}")
    print(f"Game ID: {selected_game['gameId']}")
    print(f"Prediction Key: {selected_game['prediction_key']}")

    # WebSocket URL'sini kullanıcıdan al
    websocket_url = input("Lütfen WebSocket URL'sini girin: ")

    # WebSocket bağlantısını ayrı bir thread'de başlat
    websocket_thread = threading.Thread(
        target=connect_socket,
        args=(websocket_url, selected_game)
    )
    websocket_thread.start()

if __name__ == "__main__":
    main()