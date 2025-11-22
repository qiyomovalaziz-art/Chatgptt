import os
import logging
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from openai import OpenAI
import asyncio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment variables
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "").strip()
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "").strip()
WEBHOOK_URL = os.environ.get("WEBHOOK_URL", "").strip()

# Agar token bo‘sh bo‘lsa — darrov xato chiqaradi (Railway'da muammoni topish osonroq bo‘ladi)
if not TELEGRAM_TOKEN:
    raise ValueError("❌ TELEGRAM_TOKEN topilmadi. Railway → Variables bo‘limida kiriting.")
if not OPENAI_API_KEY:
    raise ValueError("❌ OPENAI_API_KEY topilmadi.")
if not WEBHOOK_URL:
    raise ValueError("❌ WEBHOOK_URL topilmadi.")

client = OpenAI(api_key=OPENAI_API_KEY)

app = Flask(__name__)
telegram_app = Application.builder().token(TELEGRAM_TOKEN).build()


# ---------------- Telegram handlerlar ----------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salom! Men ChatGPT yordamchisiman. Savolingizni yozing.")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    await context.bot.send_chat_action(chat_id=update.message.chat_id, action="typing")

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Siz foydali yordamchi botsiz."},
                {"role": "user", "content": user_text}
            ],
            max_tokens=300
        )

        answer = response.choices[0].message["content"]
        await update.message.reply_text(answer)

    except Exception as e:
        await update.message.reply_text(f"Xatolik: {e}")


telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))


# ---------------- Flask webhook ----------------

@app.post("/")
def webhook():
    data = request.get_json()
    update = Update.de_json(data, telegram_app.bot)
    telegram_app.update_queue.put_nowait(update)
    return "OK", 200


# ---------------- Ishga tushirish ----------------

if __name__ == "__main__":
    async def setup():
        await telegram_app.bot.set_webhook(WEBHOOK_URL)

    asyncio.run(setup())

    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
