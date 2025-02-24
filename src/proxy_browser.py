from playwright.sync_api import sync_playwright

def start_browser(selected_game):
    with sync_playwright() as playwright:
        # Tarayıcıyı başlatma ve detaylı konfigürasyon ayarları
        browser = playwright.chromium.launch(headless=False, args=["--disable-web-security", "--allow-running-insecure-content"])
        context = browser.new_context(ignore_https_errors=True)
        page = context.new_page()

        # WebSocket mesajlarını yakalama
        websocket_messages = []

        def handle_websocket(ws):
            print(f"WebSocket açıldı: {ws.url}")
            ws.on("framesent", lambda frame: websocket_messages.append(f"Sent: {frame.payload}"))
            ws.on("framereceived", lambda frame: websocket_messages.append(f"Received: {frame.payload}"))

        page.on("websocket", handle_websocket)

        # Hedef sayfaya gitme (google.com olarak ayarlıyoruz)
        page.goto("http://google.com")

        # Mesajları bir dosyaya yazma
        game_id = selected_game.get("gameId", "unknown_game")
        with open(f"websocket_messages_{game_id}.txt", "w") as file:
            for message in websocket_messages:
                file.write(message + "\n")

        # Tarayıcıyı açık tutmak için sonsuz döngü
        print("Tarayıcı açık durumda, kapatmak için manuel olarak kapatın.")
        while True:
            pass  # Tarayıcıyı açık tutmak için sonsuz döngü

if __name__ == "__main__":
    selected_game = {
        'name': 'Example Game',
        'gameId': 'example_game',
        'prediction_file': 'example_game.py',
        'data_type': 'json',
        'track_type': 'browser',
        'crash_key': 'game_result',
        'prediction_key': 'FinishRound'
    }
    start_browser(selected_game)
