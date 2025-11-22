from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime
import pytz
import os

TOKEN = "8496446032:AAF6Yxv7dnrp_qMDXegWVddgrvMQKK3q2uo"

# Rasm fayllari ro'yxati
images = ["rasm1.jpg", "rasm2.jpg", "rasm3.jpg"]

def start(update, context):
    keyboard = [
        [InlineKeyboardButton("📅 Bugungi sana", callback_data="sana")],
        [InlineKeyboardButton("⏰ Hozirgi soat", callback_data="soat")],
        [InlineKeyboardButton("🖼 Rasm yubor", callback_data="rasm_0")],
        [InlineKeyboardButton("🎥 Video yubor", callback_data="video")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Assalomu alaykum! Tugmalardan birini tanlang:", reply_markup=reply_markup)

def button(update, context):
    query = update.callback_query
    query.answer()
    
    # Toshkent vaqti
    tz = pytz.timezone("Asia/Tashkent")
    
    if query.data == "sana":
        query.edit_message_text(f"📅 Bugungi sana: {datetime.now(tz).strftime('%Y-%m-%d')}")
        
    elif query.data == "soat":
        query.edit_message_text(f"⏰ Hozirgi vaqt (Toshkent): {datetime.now(tz).strftime('%H:%M:%S')}")
        
    elif query.data.startswith("rasm"):
        index = int(query.data.split("_")[1])
        if index < len(images) and os.path.exists(images[index]):
            keyboard = []
            # Keyingi rasm tugmasi
            if index + 1 < len(images):
                keyboard = [[InlineKeyboardButton("Next ➡️", callback_data=f"rasm_{index+1}")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.message.reply_photo(open(images[index], "rb"), caption=f"Rasm {index+1}", reply_markup=reply_markup)
        else:
            query.message.reply_text("Rasm topilmadi yoki oxirgi rasm!")
    
    elif query.data == "video":
        if os.path.exists("video.mp4"):
            query.message.reply_video(open("video.mp4", "rb"), caption="Mana video 🎥")
        else:
            query.message.reply_text("Video topilmadi!")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))
    
    print("Bot ishga tushdi...")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
