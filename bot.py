import asyncio
import random
import requests
from playwright.async_api import async_playwright

URL = "https://www.ticketswap.com/concert-tickets/don-west-amsterdam-paradiso-2026-06-17-CYF7F4cWrLcqofDFpcWRD"

BOT_TOKEN = "8738920216:AAEOzRC44zlGC48kQKNQoSthJNuYPk4NB-U"
CHAT_ID = "8623302349"

already_found = False


def send(msg):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": msg},
        timeout=10,
    )


async def main():
    global already_found

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu",
                "--disable-software-rasterizer",
                "--disable-extensions",
                "--disable-background-networking",
                "--disable-background-timer-throttling",
                "--disable-renderer-backgrounding",
                "--disable-features=site-per-process",
                "--single-process",
                "--no-zygote",
            ],
        )

        page = await browser.new_page(
            viewport={"width": 1365, "height": 768},
            user_agent=(
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
        )
        
        while True:
            try:
                print("Checking with browser...", flush=True)

                await page.goto(URL, wait_until="domcontentloaded", timeout=45000)
                await page.wait_for_timeout(1500)

                text = (await page.locator("body").inner_text()).lower()

                keywords = [
                    "buy ticket",
                    "get ticket",
                    "available",
                    "koop ticket",
                    "ticket available",
                ]

                sold_out_keywords = [
                    "no tickets available",
                    "sold out",
                    "nothing available",
                    "notify me",
                ]

                found = any(k in text for k in keywords)
                sold_out = any(k in text for k in sold_out_keywords)

                if found and not sold_out and not already_found:
                    already_found = True
                    print("FOUND!", flush=True)
                    send(
                        "🚨 TICKET DISPONIBILE!\n"
                        "APRIRE IMMEDIATAMENTE:\n"
                        f"{URL}"
                    )

                elif not found:
                    already_found = False
                    print("No tickets", flush=True)

                else:
                    print("Page checked", flush=True)

            except Exception as e:
                print(f"ERROR: {e}", flush=True)

            await asyncio.sleep(random.uniform(2.0, 3.0))


asyncio.run(main())
