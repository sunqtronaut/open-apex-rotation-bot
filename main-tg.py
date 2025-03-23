import requests
from bs4 import BeautifulSoup
import os
# from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

from flask import Flask, redirect

# Flask application for a health check
app = Flask(__name__)

@app.route("/")
def home():
    return "This is a Telegram bot for Apex Legends map rotation. Use it in Telegram https://t.me/@openapexrotation_bot to get map schedules."

@app.route("/redirect")
def redirect_to_base():
    return redirect(BASE_URL, code=302)

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


def fetch_html(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def parse_schedule(html, map_name):
    soup = BeautifulSoup(html, 'html.parser')
    sections = soup.find_all('div', style=lambda value: value and 'background' in value)
    # print(f"Found {len(sections)} sections for map {map_name}")  # Debug print
    schedule = []
    for section in sections:
        map_title = section.find('h3').text.strip()
        if map_title == map_name:
            time_info = section.find('p').text.strip()
            if 'From' in time_info and 'to' in time_info and ('starts in' in time_info or 'ends in' in time_info):
                schedule.append(time_info)
    return schedule

def format_schedule(schedule, mode, url):
    output = [f"{mode} {MAP_NAME}: {url}"]
    for entry in schedule:
        output.append(f"{entry}")
    return "\n".join(output)

def get_schedule(map_name):
    print("All times are in UTC")

    pubs_html = fetch_html(PUBS_URL)
    pubs_schedule = parse_schedule(pubs_html, map_name)
    pubs_output = format_schedule(pubs_schedule, "PUBS", PUBS_URL)

    ranked_html = fetch_html(RANKED_URL)
    ranked_schedule = parse_schedule(ranked_html, map_name)
    ranked_output = format_schedule(ranked_schedule, "RANKED", RANKED_URL)

    return f"{pubs_output}\n\n{ranked_output}"

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Send /get <mapname> to get the schedule for a specific map.')

async def get(update: Update, context: CallbackContext) -> None:
    if len(context.args) == 0:
        await update.message.reply_text('Please provide a map name.')
        return

    map_name = ' '.join(context.args)
    schedule = get_schedule(map_name)
    await update.message.reply_text(schedule, disable_web_page_preview=True)

# load_dotenv()
# BASE_URL = os.getenv('BASE_URL', "https://apexlegendsstatus.com/current-map/battle_royale")
# MAP_NAME = os.getenv('MAP_NAME', "Kings Canyon")
# TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

BASE_URL = os.environ.get('BASE_URL', "https://apexlegendsstatus.com/current-map/battle_royale")
MAP_NAME = os.environ.get('MAP_NAME', "Kings Canyon")
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')

PUBS_URL = f"{BASE_URL}/pubs"
RANKED_URL = f"{BASE_URL}/ranked"

if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN is not set. Please set it in the .env file.")

from threading import Thread

def main():
    def run_telegram_bot():
        application = Application.builder().token(TELEGRAM_TOKEN).build()
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("get", get))
        application.run_polling(poll_interval=1.0)

    flask_thread = Thread(target=run_flask)
    flask_thread.start()

    run_telegram_bot()

if __name__ == "__main__":
    main()
