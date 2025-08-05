# 🔸 handlers/welcome.py
from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

async def welcome_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for user in update.message.new_chat_members:
        name = user.first_name
        await update.message.reply_text(f"🎉 خوش آمدی {name}!")

def register_handlers(app):
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_user))
