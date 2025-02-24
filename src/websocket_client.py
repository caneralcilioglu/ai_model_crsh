import websocket
import json
import sys
import os
import base64
import uuid

# PYTHONPATH ayarları
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.save_records import save_data

ws = None  # WebSocket bağlantısını global olarak sakla

def log_raw_message(message):
    with open("raw_messages.txt", "a") as file:
        file.write(message + "\n")

def on_message(ws, message):
    # Mesajın sonundaki `ASCII 30` karakterini temizle
    cleaned_message = message.replace("\x1e", "")
    log_raw_message(cleaned_message)
    print(f"Gelen veri: {cleaned_message}")

    try:
        data = json.loads(cleaned_message)
        if selected_game["prediction_key"] in cleaned_message:
            print(f"Tahmin tetikleyici mesaj: {cleaned_message}")
            save_data(data, selected_game["gameId"])
            train_model(selected_game["gameId"])
    except json.JSONDecodeError as e:
        print(f"Hata: Geçersiz JSON formatı. Mesaj: {cleaned_message}, Hata: {str(e)}")

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

def generate_sec_websocket_key():
    return base64.b64encode(uuid.uuid4().bytes).decode('utf-8').strip()

def connect_socket(url, selected_game):
    global ws
    ws = websocket.WebSocketApp(
        url,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
        header=[
            "Accept-Encoding: gzip, deflate, br, zstd",
            "Accept-Language: tr,en-US;q=0.9,en;q=0.8,id;q=0.7",
            "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
            "Cache-Control: no-cache",
            "Connection: Upgrade", 
            "Pragma: no-cache", 
            "Upgrade: websocket"
        ]
    )
    ws.on_open = on_open
    ws.run_forever(sslopt={"cert_reqs": 0})

if __name__ == "__main__":
    pass
