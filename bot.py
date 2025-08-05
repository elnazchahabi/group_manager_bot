# 🔸 bot.py
from telegram.ext import ApplicationBuilder
from config import BOT_TOKEN

from handlers import welcome, moderation, admin

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    admin.register_handlers(app)
    welcome.register_handlers(app)
    moderation.register_handlers(app)
    # admin.register_handlers(app)

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()

