import os
from telegram import Update, ForceReply
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "8171726902"))

pending_ads = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        "📢 Reklama yubormoqchimisiz? Matningizni bu yerga yozing. Admin siz bilan aloqaga chiqadi."
    )

async def receive_ad(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    message = update.message.text
    pending_ads[user.id] = message

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"📥 Yangi reklama so'rovi:\n👤 Foydalanuvchi: @{user.username} ({user.id})\n✉️ Xabar: {message}"
    )

    await update.message.reply_text("✅ So‘rovingiz qabul qilindi. Tez orada admin siz bilan bog‘lanadi.")

async def reply_to_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    try:
        text = update.message.text
        if not text.startswith("/reply"):
            return

        _, user_id, *msg = text.split(" ")
        user_id = int(user_id)
        message = " ".join(msg)
        await context.bot.send_message(chat_id=user_id, text=f"📩 Admin javobi:\n{message}")
        await update.message.reply_text("✅ Javob yuborildi.")
    except Exception as e:
        await update.message.reply_text(f"❌ Xatolik: {e}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, receive_ad))
    app.add_handler(MessageHandler(filters.TEXT & filters.COMMAND, reply_to_user))
    app.run_polling()

if __name__ == '__main__':
    main()
