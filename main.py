import time
import requests
from config import COIN, THRESHOLD, TELEGRAM_TOKEN, CHAT_ID

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

def get_price():
    url = f"https://api.bitvavo.com/v2/ticker/price?market={COIN}"
    r = requests.get(url)
    return float(r.json()["price"])

def main():
    alerted = False  # voorkomt spam

    while True:
        price = get_price()

        if price > THRESHOLD and not alerted:
            send_telegram(f"🚀 {COIN} staat boven {THRESHOLD}! Huidige prijs: {price}")
            alerted = True

        if price <= THRESHOLD:
            alerted = False  # reset zodat je opnieuw een alert krijgt

        time.sleep(5)

if __name__ == "__main__":
    main()
