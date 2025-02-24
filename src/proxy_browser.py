from playwright.sync_api import sync_playwright
import json

def handle_ws_message(ws_message):
    print(f"WebSocket mesajı: {ws_message.text}")

def start_browser(selected_game):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # İlk olarak google.com'u açın
        page.goto("https://google.com")
        
        # Kullanıcının siteye ulaşması ve login olması için yeterli süre bekleyin
        input("Siteye ulaşın ve login olun, ardından devam etmek için Enter tuşuna basın...")

        # WebSocket URL'sini dinleyin
        ws_url = input("Lütfen WebSocket URL'sini girin: ")

        # Belirli WebSocket URL'sini dinlemek için filtreleme ekleyin
        context.on("websocket", lambda ws: ws.url == ws_url and ws.on("framereceived", handle_ws_message))

        # Tarayıcıyı kapatmadan önce yeterli süre bekleyin
        page.wait_for_timeout(60000)  # 60 saniye bekler

        browser.close()
