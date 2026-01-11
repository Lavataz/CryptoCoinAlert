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
    # Houdt bij welke coins al een alert hebben verstuurd
    alerted = {pair["coin"]: False for pair in PAIRS}

    while True:
        for pair in PAIRS:
            coin = pair["coin"]
            threshold = pair["threshold"]

            price = get_price(coin)

            # Check of prijs boven threshold komt
            if price > threshold and not alerted[coin]:
                send_telegram(f"🚀 {coin} staat boven {threshold}! Huidige prijs: {price}")
                alerted[coin] = True

            # Reset wanneer prijs weer onder threshold komt
            if price <= threshold:
                alerted[coin] = False

        time.sleep(5)

if __name__ == "__main__":
    main()