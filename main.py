from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
import os

load_dotenv()
# Initialize the Telegram bot
TOKEN: Final = os.getenv("BOT_TOKEN")
BOT_USERNAME: Final = os.getenv("BOT_USERNAME")  # No '@' for easier matching

# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Hello, {update.effective_user.full_name}!\nI am @{BOT_USERNAME}.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Is there anything else I can help you with?")

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("This is a custom command.")

# Responses
def handle_response(text: str) -> str:
    processed = text.lower()

    if 'hello' in processed:
        return "Hello!"
    if 'how are you' in processed:
        return "I am doing well, thank you!"
    if 'goodbye' in processed:
        return "Goodbye!"

    return "I don't understand that."

# Message Handlers
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type = update.message.chat.type
    text = update.message.text
    user_id = update.message.chat.id
    print(f"User ({user_id}) in {message_type}: {text}")

    response = "I didn't understand that."  # Default response
    if message_type == 'group':
        if f"@{BOT_USERNAME}" in text:
            next_text = text.replace(f"@{BOT_USERNAME}", "").strip()
            response = handle_response(next_text)
    else:
        response = handle_response(text)

    print("Bot:", response)
    await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"An error occurred: {context.error}")
    import traceback
    traceback.print_exc()

if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Error Handling
    app.add_error_handler(error)

    # Polling
    print("Bot is running...")
    app.run_polling(poll_interval=3)
