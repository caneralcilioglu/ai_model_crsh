import websocket
import json
import threading
from utils.save_records import save_data  # Doğru içe aktarma
from src.model_training import train_model  # Doğru içe aktarma

ws = None  # WebSocket bağlantısını global olarak sakla

def connect_socket(url, selected_game):
    """WebSocket bağlantısını kurar ve gelen mesajları işler."""
    global ws

    def on_message(ws, message):
        print(f"Gelen veri: {message}")
        try:
            data = json.loads(message)
            # Eğer mesaj, seçilen oyunun prediction_key'ini içeriyorsa
            if selected_game["prediction_key"] in message:
                print(f"Tahmin tetikleyici mesaj: {message}")
                # Veriyi kaydet
                save_data(data, selected_game["gameId"])
                # Modeli eğit
                train_model(selected_game["gameId"])
        except json.JSONDecodeError:
            print("Hata: Geçersiz JSON formatı.")

    def on_error(ws, error):
        print(f"Hata: {error}")

    def on_close(ws, close_status_code, close_msg):
        print("WebSocket bağlantısı kapatıldı")

    def on_open(ws):
        print("WebSocket bağlantısı kuruldu")
        # Bağlantı açıldığında başlangıç mesajlarını gönder
        ws.send(json.dumps({"protocol": "json", "version": 1}))
        ws.send(json.dumps({"type": 6}))
        ws.send(json.dumps({
            "arguments": [{
                "version": 2,
                "activeGameId": "7",
                "token": "",
                "isDemo": "true",
                "partnerId": "488",
                "culture": "tr"
            }],
            "invocationId": "0",
            "target": "GetInitialState",
            "type": 1
        }))

    ws = websocket.WebSocketApp(url,
                               on_message=on_message,
                               on_error=on_error,
                               on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()