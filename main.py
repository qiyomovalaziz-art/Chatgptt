# file: tg_chatgpt_bot.py
import os
import logging
import asyncio

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# OpenAI -- rasmiy mijozdan foydalanamiz
# agar openai kutubxonasining yangi interfeysi boshqacha bo'lsa, docsga qarang:
# https://platform.openai.com/docs/quickstart  va API reference. 
from openai import OpenAI

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

if not OPENAI_API_KEY or not TELEGRAM_TOKEN:
    raise RuntimeError("Iltimos, OPENAI_API_KEY va TELEGRAM_TOKEN environment o'zgaruvchilarini belgilang.")

# OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Oddiy start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Salom! Men ChatGPT-ussuli botman. Menga savol yozing va men OpenAI orqali javob beraman."
    )

# Help komandasi
async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Faqat xabar yozing — men OpenAI yordamida javob beraman.")

# Asosiy xabarni qabul qilib, OpenAI ga so'rov jo'natadi
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    chat_id = update.message.chat_id

    # qisqa "typing" holatini ko'rsatish
    await context.bot.send_chat_action(chat_id=chat_id, action="typing")

    try:
        # OpenAI Chat Completion chaqirig'i (oddiy misol)
        # Docs: platform.openai.com/docs/api-reference/chat
        resp = client.chat.completions.create(
            model="gpt-4o-mini",  # yerni o'zgartirishingiz mumkin (docsga qarang)
            messages=[
                {"role": "system", "content": "Siz yordamchi botsiz. Javoblar qisqa va foydali bo'lsin."},
                {"role": "user", "content": user_text},
            ],
            max_tokens=800,
            temperature=0.7,
        )

        # Javob matnini olish
        # struktura: resp.choices[0].message.content  (API versiyasiga qarab farq bo'lishi mumkin)
        answer = ""
        if resp and getattr(resp, "choices", None):
            answer = resp.choices[0].message["content"].strip()
        else:
            answer = "Kechirasiz, hozir javob olishda muammo bo'ldi."

        # Telegramga javob yuborish
        await update.message.reply_text(answer)

    except Exception as e:
        logger.exception("OpenAI so'rovida xato:")
        await update.message.reply_text("Xatolik yuz berdi: " + str(e))


def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Bot ishga tushmoqda...")
    app.run_polling(allowed_updates=["message"])

if __name__ == "__main__":
    main()
