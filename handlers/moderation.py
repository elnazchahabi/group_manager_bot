import os
import re
from telegram import Update
from telegram.ext import MessageHandler, filters, ContextTypes

# بارگذاری کلمات ممنوع
BANNED_WORDS_PATH = os.path.join("data", "banned_words.txt")
BANNED_WORDS = [w.strip().lower() for w in open(BANNED_WORDS_PATH, encoding="utf-8")]

# الگوی لینک
link_pattern = re.compile(r"(https?://|www\.|t\.me/|telegram\.me/)\S+", re.IGNORECASE)

async def filter_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message or not message.text:
        return

    text = message.text.lower()

    # بررسی فحش
    for word in BANNED_WORDS:
        if re.search(r"\b" + re.escape(word) + r"\b", text):

            await message.delete()
            await context.bot.send_message(chat_id=message.chat.id, text="⛔️ پیام حاوی کلمات نامناسب بود و حذف شد.")
            return

    # بررسی لینک
    if link_pattern.search(text):
        await message.delete()
        await context.bot.send_message(chat_id=message.chat.id, text="🚫 ارسال لینک مجاز نیست.")
        return

    # بررسی فوروارد
    if message.forward_date:
        await message.delete()
        await context.bot.send_message(chat_id=message.chat.id, text="🚫 پیام فوروارد شده مجاز نیست.")
        return

# فقط اینو ثبت کن
def register_handlers(app):
    app.add_handler(MessageHandler(filters.TEXT | filters.FORWARDED, filter_all))
