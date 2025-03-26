import os
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from telegram.ext import Application, CallbackQueryHandler, CallbackContext, CommandHandler
from dotenv import load_dotenv

load_dotenv()

# Base URL and Telegram token from environment variables
BASE_URL = os.getenv('BASE_URL', "https://apexlegendsstatus.com/current-map/battle_royale")
TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

PUBS_URL = f"{BASE_URL}/pubs"
RANKED_URL = f"{BASE_URL}/ranked"

if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN is not set. Please set it in the environment variables.")

# Fetch HTML content from a URL
async def fetch_html(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                return await response.text()
    except aiohttp.ClientError as e:
        print(f"Error fetching URL {url}: {e}")
        return None

# Parse the schedule for a specific map
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

# Format the schedule into a readable string
def format_schedule(schedule, mode, url):
    output = [f"{mode} {url}"]
    for entry in schedule:
        output.append(f"{entry}")
    return "\n".join(output)

# Get the schedule for a specific map
async def get_schedule(map_name):
    pubs_html = await fetch_html(PUBS_URL)
    if not pubs_html:
        return "Error fetching PUBS schedule."

    pubs_schedule = parse_schedule(pubs_html, map_name)
    pubs_output = format_schedule(pubs_schedule, "PUBS", PUBS_URL)

    ranked_html = await fetch_html(RANKED_URL)
    if not ranked_html:
        return "Error fetching RANKED schedule."

    ranked_schedule = parse_schedule(ranked_html, map_name)
    ranked_output = format_schedule(ranked_schedule, "RANKED", RANKED_URL)

    return f"{pubs_output}\n\n{ranked_output}"

# Show buttons for map selection
async def show_buttons(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [
            InlineKeyboardButton("Kings Canyon", callback_data="Kings Canyon"),
            InlineKeyboardButton("Worlds Edge", callback_data="Worlds Edge"),
        ],
        [
            InlineKeyboardButton("Broken Moon", callback_data="Broken Moon"),
            InlineKeyboardButton("Olympus", callback_data="Olympus"),
        ],
        [
            InlineKeyboardButton("Storm Point", callback_data="Storm Point"),
            InlineKeyboardButton("E-District", callback_data="E-District"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:
        await update.message.reply_text("Choose a map:", reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.edit_message_text("Choose a map:", reply_markup=reply_markup)

# Handle button clicks
async def button_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()  # Acknowledge the button press

    map_name = query.data
    if not map_name:
        await query.edit_message_text("Invalid map selection.")
        return

    schedule = await get_schedule(map_name)
    await query.edit_message_text(schedule, disable_web_page_preview=True)

# Handle the /start command
async def start_command(update: Update, context: CallbackContext) -> None:
    if update.effective_chat.type == "private":
        await show_buttons(update, context)
    else:
        await update.message.reply_text("This bot is designed for private chats. Use it in a private chat to see the map selection menu.")

# Handle the /help command
async def help_command(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        "Here are the available commands:\n"
        "/start - Start the bot and see the map selection menu\n"
        "/schedule - View the map rotation schedule\n"
        "/help - Show this help message"
    )

# Run the Telegram bot
async def run_telegram_bot():
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Set bot commands (for menu in Telegram)
    commands = [
        BotCommand("start", "Start the bot and see the map selection menu"),
        BotCommand("schedule", "View the map rotation schedule"),
        BotCommand("help", "Show help information"),
    ]
    await application.bot.set_my_commands(commands)

    # Add handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("schedule", show_buttons))
    application.add_handler(CallbackQueryHandler(button_handler))

    # Start polling
    await application.run_polling(poll_interval=1.0, drop_pending_updates=True)

# Main entry point
if __name__ == "__main__":
    import nest_asyncio
    nest_asyncio.apply()  # Fix for environments with already running event loops
    asyncio.run(run_telegram_bot())
