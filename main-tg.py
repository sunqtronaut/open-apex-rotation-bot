import requests
from bs4 import BeautifulSoup
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CallbackQueryHandler, CallbackContext, MessageHandler, filters
from flask import Flask

# Flask application for health check
app = Flask(__name__)

@app.route("/")
def health_check():
    return "Health check: OK", 200

def fetch_html(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def parse_schedule(html, map_name):
    soup = BeautifulSoup(html, 'html.parser')
    sections = soup.find_all('div', style=lambda value: value and 'background' in value)
    schedule = []
    for section in sections:
        map_title = section.find('h3').text.strip()
        if map_title == map_name:
            time_info = section.find('p').text.strip()
            if 'From' in time_info and 'to' in time_info and ('starts in' in time_info or 'ends in' in time_info):
                schedule.append(time_info)
    return schedule

def format_schedule(schedule, mode, url):
    output = [f"{mode} {url}"]
    for entry in schedule:
        output.append(f"{entry}")
    return "\n".join(output)

def get_schedule(map_name):
    pubs_html = fetch_html(PUBS_URL)
    pubs_schedule = parse_schedule(pubs_html, map_name)
    pubs_output = format_schedule(pubs_schedule, "PUBS", PUBS_URL)

    ranked_html = fetch_html(RANKED_URL)
    ranked_schedule = parse_schedule(ranked_html, map_name)
    ranked_output = format_schedule(ranked_schedule, "RANKED", RANKED_URL)

    return f"{pubs_output}\n\n{ranked_output}"

async def show_buttons(update: Update, context: CallbackContext) -> None:
    # Create buttons for map selection
    keyboard = [
        [InlineKeyboardButton("Kings Canyon", callback_data="Kings Canyon")],
        [InlineKeyboardButton("Worlds Edge", callback_data="Worlds Edge")],
        [InlineKeyboardButton("Broken Moon", callback_data="Broken Moon")],
        [InlineKeyboardButton("Olympys", callback_data="Olympys")],
        [InlineKeyboardButton("Storm Point", callback_data="Storm Point")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Choose a map:", reply_markup=reply_markup)

async def button_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()  # Acknowledge the button press

    # Get the map name from callback_data
    map_name = query.data
    schedule = get_schedule(map_name)

    # Send the schedule
    await query.edit_message_text(schedule, disable_web_page_preview=True)

BASE_URL = os.environ.get('BASE_URL', "https://apexlegendsstatus.com/current-map/battle_royale")
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')

PUBS_URL = f"{BASE_URL}/pubs"
RANKED_URL = f"{BASE_URL}/ranked"

if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN is not set. Please set it in the environment variables.")

from threading import Thread

def run_telegram_bot():
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Add handlers
    application.add_handler(CallbackQueryHandler(button_handler))  # Handle button clicks
    application.add_handler(MessageHandler(filters.ALL, show_buttons))  # Show buttons for any interaction

    # Start polling
    application.run_polling(poll_interval=1.0, drop_pending_updates=True)

def run_health_check():
    port = int(os.environ.get("PORT", 5000))  # Render uses the PORT environment variable
    app.run(host="0.0.0.0", port=port)

def main():
    # Run Flask health check and Telegram bot in parallel
    flask_thread = Thread(target=run_health_check)
    flask_thread.start()

    run_telegram_bot()

if __name__ == "__main__":
    main()
