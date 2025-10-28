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


# ---- Run the bot ----
if __name__ == '__main__':
    print("Bot is running...")
    bot.polling(none_stop=True)
