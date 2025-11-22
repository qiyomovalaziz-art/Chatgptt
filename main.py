from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from datetime import datetime
import os

# BOT TOKENINI SHU YERGA YOZING
TOKEN = "8496446032:AAF6Yxv7dnrp_qMDXegWVddgrvMQKK3q2uo"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📅 Bugungi sana", callback_data="sana")],
        [InlineKeyboardButton("⏰ Hozirgi soat", callback_data="soat")],
        [InlineKeyboardButton("🖼 Rasm yubor", callback_data="rasm")],
        [InlineKeyboardButton("🎥 Video yubor", callback_data="video")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Assalomu alaykum! Tugmalardan birini tanlang:", reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "sana":
        today = datetime.now().strftime("%Y-%m-%d")
        await query.edit_message_text(f"📅 Bugungi sana: {today}")

    elif query.data == "soat":
        now = datetime.now().strftime("%H:%M:%S")
        await query.edit_message_text(f"⏰ Hozirgi vaqt: {now}")

    elif query.data == "rasm":
        if os.path.exists("rasm.jpg"):
            await query.message.reply_photo(open("rasm.jpg", "rb"), caption="Mana rasm 🖼")
        else:
            await query.message.reply_text("Rasm topilmadi!")

    elif query.data == "video":
        if os.path.exists("video.mp4"):
            await query.message.reply_video(open("video.mp4", "rb"), caption="Mana video 🎥")
        else:
            await query.message.reply_text("Video topilmadi!")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))

    print("Bot ishga tushdi...")
    app.run_polling()

if __name__ == "__main__":
    main()
