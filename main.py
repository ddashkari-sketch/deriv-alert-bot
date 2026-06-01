from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "8469679722:AAFKwUg1KyXZG4x8X26utLWr2P54Lv0vYQo")
CHAT_ID = os.environ.get("CHAT_ID", "792435450")

INDEX_EMOJIS = {
    "crash1000": "💥 CRASH 1000",
    "crash900": "💥 CRASH 900",
    "crash600": "💥 CRASH 600",
    "crash500": "💥 CRASH 500",
    "boom1000": "🚀 BOOM 1000",
    "boom900": "🚀 BOOM 900",
    "boom600": "🚀 BOOM 600",
    "boom500": "🚀 BOOM 500",
    "boom300": "🚀 BOOM 300",
}

CHART_LINKS = {
    "crash1000": "https://www.tradingview.com/chart/?symbol=Deriv:CRASH_1000&interval=15",
    "crash900": "https://www.tradingview.com/chart/?symbol=Deriv:CRASH_900&interval=15",
    "crash600": "https://www.tradingview.com/chart/?symbol=Deriv:CRASH_600&interval=15",
    "crash500": "https://www.tradingview.com/chart/?symbol=Deriv:CRASH_500&interval=15",
    "boom1000": "https://www.tradingview.com/chart/?symbol=Deriv:BOOM_1000&interval=15",
    "boom900": "https://www.tradingview.com/chart/?symbol=Deriv:BOOM_900&interval=15",
    "boom600": "https://www.tradingview.com/chart/?symbol=Deriv:BOOM_600&interval=15",
    "boom500": "https://www.tradingview.com/chart/?symbol=Deriv:BOOM_500&interval=15",
    "boom300": "https://www.tradingview.com/chart/?symbol=Deriv:BOOM_300&interval=15",
}

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"Telegram error: {e}")

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json(force=True)
        index = str(data.get("index", "")).lower().replace(" ", "").replace("_", "")
        price = data.get("price", "N/A")
        drop = data.get("drop", "N/A")
        signal = data.get("signal", "SPIKE")
        time = data.get("time", "")
        label = INDEX_EMOJIS.get(index, f"📊 {index.upper()}")
        chart = CHART_LINKS.get(index, "https://www.tradingview.com")

        if "crash" in index:
            alert_emoji = "📉"
            alert_type = "ТОМ УНАЛТ ОРЛОО"
        else:
            alert_emoji = "📈"
            alert_type = "ТОМ ӨСӨЛТ ОРЛОО"

        message = (
            f"🚨 <b>{label}</b>\n"
            f"{alert_emoji} <b>{alert_type}!</b>\n"
            f"━━━━━━━━━━━━━━\n"
            f"💰 Үнэ: <b>{price}</b>\n"
            f"⬇️ Хэмжээ: <b>{drop}</b>\n"
            f"⏰ Цаг: {time}\n"
            f"━━━━━━━━━━━━━━\n"
            f"📊 <a href='{chart}'>15m Чарт харах</a>"
        )
        send_telegram(message)
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/test", methods=["GET"])
def test():
    send_telegram(
        "✅ <b>Deriv Alert Bot ажиллаж байна!</b>\n"
        "📊 Crash 1000/900/600/500\n"
        "📊 Boom 1000/900/600/500/300\n"
        "⚡ Бүх индексүүд хяналтад байна!\n"
        "━━━━━━━━━━━━━━\n"
        f"📊 <a href='https://www.tradingview.com/chart/?symbol=Deriv:CRASH_1000&interval=15'>Crash 1000 чарт</a>"
    )
    return jsonify({"status": "Test message sent!"}), 200

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "Deriv Alert Bot is running! 🚀"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
