import asyncio
import requests
import random
from playwright.async_api import async_playwright

URL = "https://www.ticketswap.com/concert-tickets/don-west-amsterdam-paradiso-2026-06-17-CYF7F4cWrLcqofDFpcWRD"

BOT_TOKEN = "8738920216:AAG9GwfOgP3XEZ_XmSPkWYfM-4fzeykEBTQ"
CHAT_ID = "8623302349"

already_found = False


def send(msg):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": msg
        }
    )


async def main():
    global already_found

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True
        )

        page = await browser.new_page()

        while True:
            try:
                print("Checking...", flush=True)

                await page.goto(URL)

                html = await page.content()

                keywords = [
                    "Buy ticket",
                    "Get ticket",
                    "Available",
                    "Koop ticket"
                ]

                found = any(
                    k.lower() in html.lower()
                    for k in keywords
                )

                if found and not already_found:
                    already_found = True

                    send(
                        f"🎟 TICKET DISPONIBILE!\n\n{URL}"
                    )

                    print("FOUND!", flush=True)

                elif not found:
                    already_found = False
                    print("No tickets", flush=True)

            except Exception as e:
                print(e, flush=True)

            await asyncio.sleep(
                random.uniform(2.0, 3.0)
            )


asyncio.run(main())
