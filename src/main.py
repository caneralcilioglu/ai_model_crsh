import json
import sys
import os
import threading

# PYTHONPATH ayarları
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from websocket_client import connect_socket
from game_selection import select_game

def main():
    # Oyun seçme işlemi
    selected_game = select_game()
    print(f"Seçilen Oyun: {selected_game['name']}")
    print(f"Game ID: {selected_game['gameId']}")
    print(f"Prediction Key: {selected_game['prediction_key']}")
    print(f"Track Type: {selected_game['track_type']}")

    if selected_game['track_type'] == 'socket':
        # WebSocket URL'sini kullanıcıdan al
        websocket_url = input("Lütfen WebSocket URL'sini girin: ")
        # WebSocket bağlantısını ayrı bir thread'de başlat
        websocket_thread = threading.Thread(
            target=connect_socket,
            args=(websocket_url, selected_game)
        )
        websocket_thread.start()
    elif selected_game['track_type'] == 'browser':
        # Playwright proxy yapısını başlat
        from proxy_browser import start_browser
        start_browser(selected_game)
    else:
        print("Geçersiz track_type değeri")

if __name__ == "__main__":
    main()
