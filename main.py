import os
import logging
from flask import Flask, request

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

from openai import OpenAI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API kalitlar
TELEGRAM_TOKEN = ("8496446032:AAF6Yxv7dnrp_qMDXegWVddgrvMQKK3q2uo")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")  # Railway dan olasiz

client = OpenAI(api_key=OPENAI_API_KEY)

app = Flask(__name__)

telegram_app = Application.builder().token(TELEGRAM_TOKEN).build()


# --- Telegram funksiyalar ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salom! Men ChatGPT botman. Menga savol yozing!")


async def handle_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    chat_id = update.message.chat_id

    await context.bot.send_chat_action(chat_id=chat_id, action="typing")

    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Siz foydali yordamchi botsiz."},
                {"role": "user", "content": user_text},
            ],
            max_tokens=500
        )

        answer = resp.choices[0].message["content"]
        await update.message.reply_text(answer)

    except Exception as e:
        await update.message.reply_text("Xatolik: " + str(e))


# Handlerlar
telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_msg))


# --- Flask webhook ---
@app.post("/")
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, telegram_app.bot)
    telegram_app.update_queue.put_nowait(update)
    return "OK", 200


# Railway ishga tushirish
if __name__ == "__main__":
    # Webhook o‘rnatish
    import asyncio

    async def set_webhook():
        await telegram_app.bot.set_webhook(url=WEBHOOK_URL)

    asyncio.run(set_webhook())

    # Flask serverni ishga tushirish
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
