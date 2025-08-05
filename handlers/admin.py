
# # 🔸 handlers/admin.py
# from telegram import Update
# from telegram.ext import CommandHandler, ContextTypes

# async def mute_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     if not update.message.reply_to_message:
#         await update.message.reply_text("برای سایلنت کردن باید روی پیام کاربر ریپلای کنید.")
#         return
#     user_id = update.message.reply_to_message.from_user.id
#     await context.bot.restrict_chat_member(
#         chat_id=update.message.chat_id,
#         user_id=user_id,
#         permissions={}
#     )
#     await update.message.reply_text("🔇 کاربر سایلنت شد.")

# async def ban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     if not update.message.reply_to_message:
#         await update.message.reply_text("برای بن کردن باید روی پیام کاربر ریپلای کنید.")
#         return
#     user_id = update.message.reply_to_message.from_user.id
#     await context.bot.ban_chat_member(
#         chat_id=update.message.chat_id,
#         user_id=user_id
#     )
#     await update.message.reply_text("🚫 کاربر بن شد.")

# def register_handlers(app):
#     app.add_handler(CommandHandler("mute", mute_user))
#     app.add_handler(CommandHandler("ban", ban_user))





from telegram import Update, ChatPermissions
from telegram.ext import CommandHandler, ContextTypes
import json
import os

WARN_PATH = os.path.join("data", "warnings.json")

def load_warnings():
    if os.path.exists(WARN_PATH):
        with open(WARN_PATH, encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_warnings(data):
    with open(WARN_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

async def mute_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text("برای سایلنت کردن باید روی پیام کاربر ریپلای کنید.")
        return
    user_id = update.message.reply_to_message.from_user.id
    await context.bot.restrict_chat_member(
        chat_id=update.message.chat_id,
        user_id=user_id,
        permissions=ChatPermissions(can_send_messages=False)
    )
    await update.message.reply_text("🔇 کاربر سایلنت شد.")

async def unmute_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text("برای آزاد کردن کاربر باید روی پیامش ریپلای کنید.")
        return
    user_id = update.message.reply_to_message.from_user.id
    await context.bot.restrict_chat_member(
        chat_id=update.message.chat_id,
        user_id=user_id,
        permissions=ChatPermissions(can_send_messages=True)
    )
    await update.message.reply_text("🔊 کاربر از سایلنت خارج شد.")

async def ban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text("برای بن کردن باید روی پیام کاربر ریپلای کنید.")
        return
    user_id = update.message.reply_to_message.from_user.id
    await context.bot.ban_chat_member(
        chat_id=update.message.chat_id,
        user_id=user_id
    )
    await update.message.reply_text("🚫 کاربر بن شد.")

async def warn_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text("باید روی پیام کاربر ریپلای کنید تا اخطار ثبت شود.")
        return
    user_id = str(update.message.reply_to_message.from_user.id)
    chat_id = str(update.message.chat_id)
    warnings = load_warnings()

    if chat_id not in warnings:
        warnings[chat_id] = {}
    if user_id not in warnings[chat_id]:
        warnings[chat_id][user_id] = 0

    warnings[chat_id][user_id] += 1
    count = warnings[chat_id][user_id]
    save_warnings(warnings)

    if count >= 3:
        await context.bot.ban_chat_member(chat_id=update.message.chat_id, user_id=int(user_id))
        await update.message.reply_text("⛔️ کاربر پس از 3 اخطار بن شد.")
    else:
        await update.message.reply_text(f"⚠️ اخطار {count}/3 برای کاربر ثبت شد.")

def register_handlers(app):
    app.add_handler(CommandHandler("mute", mute_user))
    app.add_handler(CommandHandler("unmute", unmute_user))
    app.add_handler(CommandHandler("ban", ban_user))
    app.add_handler(CommandHandler("warn", warn_user))
