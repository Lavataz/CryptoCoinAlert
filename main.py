import time
import requests
from config import PAIRS, TELEGRAM_TOKEN, CHAT_ID

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

def get_price(coin):
    url = f"https://api.bitvavo.com/v2/ticker/price?market={coin}"
    r = requests.get(url)
    return float(r.json()["price"])

def main():
    alerted = {pair["coin"]: False for pair in PAIRS}
    last_status_time = time.time()

    while True:
        now = time.time()

        # --- 1. Threshold checks ---
        for pair in PAIRS:
            coin = pair["coin"]
            threshold = pair["threshold"]

            price = get_price(coin)

            if price > threshold and not alerted[coin]:
                send_telegram(f"🚀 {coin} staat boven {threshold}! Huidige prijs: {price}")
                alerted[coin] = True

            if price <= threshold:
                alerted[coin] = False

        # --- 2. Status update elke 5 minuten ---
        if now - last_status_time >= 300:  # 300 sec = 5 min
            status_lines = ["📊 *Status update* (laatste 5 min):\n"]

            for pair in PAIRS:
                coin = pair["coin"]
                price = get_price(coin)
                status_lines.append(f"- {coin}: {price}")

            send_telegram("\n".join(status_lines))
            last_status_time = now

        time.sleep(5)

if __name__ == "__main__":
    main()