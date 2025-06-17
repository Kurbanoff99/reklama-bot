import os
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = "8080369597:AAEZF-2r0C5ftNXOzj3b2zxcCmncrHSoda4"
ADMIN_ID = int(os.getenv("ADMIN_ID", "8171726902"))

# Reklama matnlarini saqlash
ads = []

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        await update.message.reply_text("🛑 Faqat admin reklama yuborishi mumkin.")
        return

    await update.message.reply_text("📢 Reklama matnini yuboring. Siz yuborgan matn botga reklama sifatida saqlanadi.")

async def handle_ad(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        return

    ad_text = update.message.text.strip()
    ads.append(ad_text)
    await update.message.reply_text("✅ Reklama matni saqlandi.")

async def list_ads(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        return

    if not ads:
        await update.message.reply_text("📭 Reklama yo‘q.")
        return

    reply = "📋 Saqlangan reklamalar:\n\n"
    for i, ad in enumerate(ads, 1):
        reply += f"{i}. {ad}\n\n"
    await update.message.reply_text(reply)

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("list", list_ads))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_ad))
    app.run_polling()

if __name__ == '__main__':
    main()
