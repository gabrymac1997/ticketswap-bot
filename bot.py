import time
import random
import requests

URL = "https://www.ticketswap.com/concert-tickets/don-west-amsterdam-paradiso-2026-06-17-CYF7F4cWrLcqofDFpcWRD"

BOT_TOKEN = "8738920216:AAG9GwfOgP3XEZ_XmSPkWYfM-4fzeykEBTQ"
CHAT_ID = "8623302349"

already_found = False


def send(msg):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": msg},
        timeout=10,
    )


def check():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    r = requests.get(URL, headers=headers, timeout=20)
    html = r.text.lower()

    keywords = [
        "buy ticket",
        "get ticket",
        "available",
        "koop ticket",
    ]

    return any(k in html for k in keywords)


while True:
    try:
        print("Checking...", flush=True)

        if check():
            if not already_found:
                already_found = True
                print("FOUND!", flush=True)
                send(f"🎟 TICKET DISPONIBILE!\n\n{URL}")
        else:
            already_found = False
            print("No tickets", flush=True)

    except Exception as e:
        print(e, flush=True)

    time.sleep(random.uniform(2.5, 4.0))
