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


# ---- Button: Information ----
@bot.message_handler(func=lambda message: message.text == "Information ℹ️")
def info(message):
    """
    Sends a short description about the bot and its commands.
    """
    bot.send_message(
        message.chat.id,
        "🤖 *Translator Bot*\n\n"
        "This bot translates your messages into the language you choose.\n\n"
        "🛠 Commands:\n"
        "• /start — restart the bot\n"
        "• Set language for translating ⚙️ — choose translation language\n"
        "• Leave feedback❓ — send suggestions or ideas\n\n"
        "Just type any message and I’ll translate it!",
        parse_mode="Markdown"
    )


# ---- Button: Feedback ----
@bot.message_handler(func=lambda message: message.text == "Leave feedback❓")
def feedback(message):
    """
    Displays contact information for user feedback.
    """
    bot.send_message(
        message.chat.id,
        "✉️ You can send your feedback or suggestions here:\n"
        "📧 Email: test@gmail.com\n"
        "💻 GitHub: (add your link here)"
    )


# ---- When user presses “Set language for translating” ----
@bot.message_handler(func=lambda message: message.text == "Set language for translating ⚙️")
def choose_language(message):
    """
    Displays the list of available languages to choose from.
    """
    bot.send_message(
        message.chat.id,
        "🌍 Choose the language you want to translate to:",
        reply_markup=set_language_keyboard()
    )


# ---- Handle language selection ----
@bot.message_handler(func=lambda message: message.text in languages.keys())
def set_language(message):
    """
    Saves the user's selected translation language.
    """
    user_langs[message.chat.id] = languages[message.text]
    bot.send_message(
        message.chat.id,
        f"✅ Translation language set to {message.text}\n\n"
        "Now type any word or sentence, and I’ll translate it!"
    )


# ---- Translate all other messages ----
@bot.message_handler(func=lambda message: True)
def translate_text(message):
    """
    Translates any message user sends to their chosen target language.
    If language not chosen yet, asks user to pick one.
    """
    chat_id = message.chat.id

    # User must choose language first
    if chat_id not in user_langs:
        bot.reply_to(message, "⚙️ Please choose a language first using /start or the settings button.")
        return

    dest_lang = user_langs[chat_id]
    text = message.text

    try:
        result = translator.translate(text, dest=dest_lang)

        # If result is coroutine — await it
        if hasattr(result, "__await__"):
            import asyncio
            result = asyncio.run(result)

        bot.reply_to(
            message,
            f"💬 {result.text}\n\n"
            "You can also change the language or continue ➡ with a translation",
            reply_markup=main_keyboard()
        )
    except Exception as e:
        bot.reply_to(message, f"⚠️ Translation error: {e}")


# ---- Run the bot ----
if __name__ == '__main__':
    print("Bot is running...")
    bot.polling(none_stop=True)
