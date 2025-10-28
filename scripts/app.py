import os
from googletrans import Translator
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv

# ---- Load environment variables from .env file ----
# (You should store your TOKEN_BOT in a .env file for safety)
load_dotenv()

# ---- Initialize Telegram Bot ----
TOKEN = os.getenv("TOKEN_BOT")  # Get token from environment variables
bot = telebot.TeleBot(TOKEN)    # Create bot instance
translator = Translator()       # Create translator instance

# ---- Store user's chosen target language for translation ----
user_langs = {}

# ---- List of supported languages ----
# Keys = shown in Telegram buttons, Values = language codes for googletrans
languages = {
    "🇬🇧 English": "en",
    "🇷🇺 Russian": "ru",
    "🇫🇷 French": "fr",
    "🇩🇪 German": "de",
    "🇪🇸 Spanish": "es",
    "🇮🇹 Italian": "it",
    "🇨🇿 Czech": "cs",
    "🇵🇱 Polish": "pl",
    "🇺🇦 Ukrainian": "uk",
    "🇨🇳 Chinese": "zh-cn",
    "🇯🇵 Japanese": "ja"
}


# ---- Function: Main keyboard menu ----
def main_keyboard():
    """
    Returns the main menu keyboard users see when they start the bot.
    Includes buttons for:
    - Information
    - Leave feedback
    - Set translation language
    """
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        KeyboardButton("Information ℹ️"),
        KeyboardButton("Leave feedback❓"),
        KeyboardButton("Set language for translating ⚙️")
    )
    return markup


# ---- Function: Language selection keyboard ----
def set_language_keyboard():
    """
    Returns a keyboard with available languages for translation.
    Arranges 3 buttons per row for better readability.
    """
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [KeyboardButton(lang) for lang in languages.keys()]

    for i in range(0, len(buttons), 3):
        markup.add(*buttons[i:i + 3])

    markup.add("Back to main keyboard")
    return markup


@bot.message_handler(commands=['start'])
def start(message):
    """
    Greets the user and displays the main keyboard menu.
    """
    bot.send_message(
        message.chat.id,
        "👋 Hello! I can translate any text you send.\n\n"
        "First, choose the language you want me to translate into:",
        reply_markup=main_keyboard()
    )


# ---- Run the bot ----
if __name__ == '__main__':
    print("Bot is running...")
    bot.polling(none_stop=True)
