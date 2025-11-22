from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime

# BOT TOKENINI SHU YERGA YOZING
TOKEN = "
8496446032:AAF6Yxv7dnrp_qMDXegWVddgrvMQKK3q2uo"

def start(update, context):
    keyboard = [
        [InlineKeyboardButton("📅 Bugungi sana", callback_data="sana")],
        [InlineKeyboardButton("⏰ Hozirgi soat", callback_data="soat")],
        [InlineKeyboardButton("🖼 Rasm yubor", callback_data="rasm")],
        [InlineKeyboardButton("🎥 Video yubor", callback_data="video")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Assalomu alaykum! Tugmalardan birini tanlang:", reply_markup=reply_markup)

def button(update, context):
    query = update.callback_query
    query.answer()

    if query.data == "sana":
        today = datetime.now().strftime("%Y-%m-%d")
        query.edit_message_text(f"📅 Bugungi sana: {today}")

    elif query.data == "soat":
        now = datetime.now().strftime("%H:%M:%S")
        query.edit_message_text(f"⏰ Hozirgi vaqt: {now}")

    elif query.data == "rasm":
        query.message.reply_photo(open("rasm.jpg", "rb"), caption="Mana rasm 🖼")

    elif query.data == "video":
        query.message.reply_video(open("video.mp4", "rb"), caption="Mana video 🎥")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
