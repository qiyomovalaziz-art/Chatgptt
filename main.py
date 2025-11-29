import logging
from datetime import datetime, timezone
import holidays
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ========================
# 🔑 BOT TOKENINGIZNI SHU YERGA QO'YING
# ========================
BOT_TOKEN = "8496446032:AAF6Yxv7dnrp_qMDXegWVddgrvMQKK3q2uo"

# ========================
# 🌍 195 TA DAVLAT (Barcha BMT a'zolari + Vatikan + Falastin)
# ========================
COUNTRIES = [
    ("🇦🇫 Afghanistan", "AF"),
    ("🇦🇱 Albania", "AL"),
    ("🇩🇿 Algeria", "DZ"),
    ("🇦🇩 Andorra", "AD"),
    ("🇦🇴 Angola", "AO"),
    ("🇦🇬 Antigua and Barbuda", "AG"),
    ("🇦🇷 Argentina", "AR"),
    ("🇦🇲 Armenia", "AM"),
    ("🇦🇺 Australia", "AU"),
    ("🇦🇹 Austria", "AT"),
    ("🇦🇿 Azerbaijan", "AZ"),
    ("🇧🇸 Bahamas", "BS"),
    ("🇧🇭 Bahrain", "BH"),
    ("🇧🇩 Bangladesh", "BD"),
    ("🇧🇧 Barbados", "BB"),
    ("🇧🇾 Belarus", "BY"),
    ("🇧🇪 Belgium", "BE"),
    ("🇧🇿 Belize", "BZ"),
    ("🇧🇯 Benin", "BJ"),
    ("🇧🇹 Bhutan", "BT"),
    ("🇧🇴 Bolivia", "BO"),
    ("🇧🇦 Bosnia and Herzegovina", "BA"),
    ("🇧🇼 Botswana", "BW"),
    ("🇧🇷 Brazil", "BR"),
    ("🇧🇳 Brunei", "BN"),
    ("🇧🇬 Bulgaria", "BG"),
    ("🇧🇫 Burkina Faso", "BF"),
    ("🇧🇮 Burundi", "BI"),
    ("🇨🇻 Cape Verde", "CV"),
    ("🇰🇭 Cambodia", "KH"),
    ("🇨🇲 Cameroon", "CM"),
    ("🇨🇦 Canada", "CA"),
    ("🇨🇫 Central African Republic", "CF"),
    ("🇹🇩 Chad", "TD"),
    ("🇨🇱 Chile", "CL"),
    ("🇨🇳 China", "CN"),
    ("🇨🇴 Colombia", "CO"),
    ("🇰🇲 Comoros", "KM"),
    ("🇨🇬 Congo", "CG"),
    ("🇨🇩 DR Congo", "CD"),
    ("🇨🇷 Costa Rica", "CR"),
    ("🇨🇮 Côte d’Ivoire", "CI"),
    ("🇭🇷 Croatia", "HR"),
    ("🇨🇺 Cuba", "CU"),
    ("🇨🇾 Cyprus", "CY"),
    ("🇨🇿 Czechia", "CZ"),
    ("🇩🇰 Denmark", "DK"),
    ("🇩🇯 Djibouti", "DJ"),
    ("🇩🇲 Dominica", "DM"),
    ("🇩🇴 Dominican Republic", "DO"),
    ("🇪🇨 Ecuador", "EC"),
    ("🇪🇬 Egypt", "EG"),
    ("🇸🇻 El Salvador", "SV"),
    ("🇬🇶 Equatorial Guinea", "GQ"),
    ("🇪🇷 Eritrea", "ER"),
    ("🇪🇪 Estonia", "EE"),
    ("🇸🇿 Eswatini", "SZ"),
    ("🇪🇹 Ethiopia", "ET"),
    ("🇫🇯 Fiji", "FJ"),
    ("🇫🇮 Finland", "FI"),
    ("🇫🇷 France", "FR"),
    ("🇬🇦 Gabon", "GA"),
    ("🇬🇲 Gambia", "GM"),
    ("🇬🇪 Georgia", "GE"),
    ("🇩🇪 Germany", "DE"),
    ("🇬🇭 Ghana", "GH"),
    ("🇬🇷 Greece", "GR"),
    ("🇬🇩 Grenada", "GD"),
    ("🇬🇹 Guatemala", "GT"),
    ("🇬🇳 Guinea", "GN"),
    ("🇬🇼 Guinea-Bissau", "GW"),
    ("🇬🇾 Guyana", "GY"),
    ("🇭🇹 Haiti", "HT"),
    ("🇻🇦 Holy See (Vatican)", "VA"),
    ("🇭🇳 Honduras", "HN"),
    ("🇭🇺 Hungary", "HU"),
    ("🇮🇸 Iceland", "IS"),
    ("🇮🇳 India", "IN"),
    ("🇮🇩 Indonesia", "ID"),
    ("🇮🇷 Iran", "IR"),
    ("🇮🇶 Iraq", "IQ"),
    ("🇮🇪 Ireland", "IE"),
    ("🇮🇱 Israel", "IL"),
    ("🇮🇹 Italy", "IT"),
    ("🇯🇲 Jamaica", "JM"),
    ("🇯🇵 Japan", "JP"),
    ("🇯🇴 Jordan", "JO"),
    ("🇰🇿 Kazakhstan", "KZ"),
    ("🇰🇪 Kenya", "KE"),
    ("🇰🇮 Kiribati", "KI"),
    ("🇰🇵 North Korea", "KP"),
    ("🇰🇷 South Korea", "KR"),
    ("🇽🇰 Kosovo", "XK"),
    ("🇰🇼 Kuwait", "KW"),
    ("🇰🇬 Kyrgyzstan", "KG"),
    ("🇱🇦 Laos", "LA"),
    ("🇱🇻 Latvia", "LV"),
    ("🇱🇧 Lebanon", "LB"),
    ("🇱🇸 Lesotho", "LS"),
    ("🇱🇷 Liberia", "LR"),
    ("🇱🇾 Libya", "LY"),
    ("🇱🇮 Liechtenstein", "LI"),
    ("🇱🇹 Lithuania", "LT"),
    ("🇱🇺 Luxembourg", "LU"),
    ("🇲🇬 Madagascar", "MG"),
    ("🇲🇼 Malawi", "MW"),
    ("🇲🇾 Malaysia", "MY"),
    ("🇲🇻 Maldives", "MV"),
    ("🇲🇱 Mali", "ML"),
    ("🇲🇹 Malta", "MT"),
    ("🇲🇭 Marshall Islands", "MH"),
    ("🇲🇷 Mauritania", "MR"),
    ("🇲🇺 Mauritius", "MU"),
    ("🇲🇽 Mexico", "MX"),
    ("🇫🇲 Micronesia", "FM"),
    ("🇲🇩 Moldova", "MD"),
    ("🇲🇨 Monaco", "MC"),
    ("🇲🇳 Mongolia", "MN"),
    ("🇲🇪 Montenegro", "ME"),
    ("🇲🇦 Morocco", "MA"),
    ("🇲🇿 Mozambique", "MZ"),
    ("🇲🇲 Myanmar", "MM"),
    ("🇳🇦 Namibia", "NA"),
    ("🇳🇷 Nauru", "NR"),
    ("🇳🇵 Nepal", "NP"),
    ("🇳🇱 Netherlands", "NL"),
    ("🇳🇿 New Zealand", "NZ"),
    ("🇳🇮 Nicaragua", "NI"),
    ("🇳🇪 Niger", "NE"),
    ("🇳🇬 Nigeria", "NG"),
    ("🇲🇰 North Macedonia", "MK"),
    ("🇳🇴 Norway", "NO"),
    ("🇴🇲 Oman", "OM"),
    ("🇵🇰 Pakistan", "PK"),
    ("🇵🇼 Palau", "PW"),
    ("🇵🇸 Palestine", "PS"),
    ("🇵🇦 Panama", "PA"),
    ("🇵🇬 Papua New Guinea", "PG"),
    ("🇵🇾 Paraguay", "PY"),
    ("🇵🇪 Peru", "PE"),
    ("🇵🇭 Philippines", "PH"),
    ("🇵🇱 Poland", "PL"),
    ("🇵🇹 Portugal", "PT"),
    ("🇶🇦 Qatar", "QA"),
    ("🇷🇴 Romania", "RO"),
    ("🇷🇺 Russia", "RU"),
    ("🇷🇼 Rwanda", "RW"),
    ("🇰🇳 Saint Kitts and Nevis", "KN"),
    ("🇱🇨 Saint Lucia", "LC"),
    ("🇻🇨 Saint Vincent and the Grenadines", "VC"),
    ("🇼🇸 Samoa", "WS"),
    ("🇸🇲 San Marino", "SM"),
    ("🇸🇹 Sao Tome and Principe", "ST"),
    ("🇸🇦 Saudi Arabia", "SA"),
    ("🇸🇳 Senegal", "SN"),
    ("🇷🇸 Serbia", "RS"),
    ("🇸🇨 Seychelles", "SC"),
    ("🇸🇱 Sierra Leone", "SL"),
    ("🇸🇬 Singapore", "SG"),
    ("🇸🇰 Slovakia", "SK"),
    ("🇸🇮 Slovenia", "SI"),
    ("🇸🇧 Solomon Islands", "SB"),
    ("🇸🇴 Somalia", "SO"),
    ("🇿🇦 South Africa", "ZA"),
    ("🇸🇸 South Sudan", "SS"),
    ("🇪🇸 Spain", "ES"),
    ("🇱🇰 Sri Lanka", "LK"),
    ("🇸🇩 Sudan", "SD"),
    ("🇸🇷 Suriname", "SR"),
    ("🇸🇪 Sweden", "SE"),
    ("🇨🇭 Switzerland", "CH"),
    ("🇸🇾 Syria", "SY"),
    ("🇹🇯 Tajikistan", "TJ"),
    ("🇹🇿 Tanzania", "TZ"),
    ("🇹🇭 Thailand", "TH"),
    ("🇹🇱 Timor-Leste", "TL"),
    ("🇹🇬 Togo", "TG"),
    ("🇹🇴 Tonga", "TO"),
    ("🇹🇹 Trinidad and Tobago", "TT"),
    ("🇹🇳 Tunisia", "TN"),
    ("🇹🇷 Turkey", "TR"),
    ("🇹🇲 Turkmenistan", "TM"),
    ("🇹🇻 Tuvalu", "TV"),
    ("🇺🇬 Uganda", "UG"),
    ("🇺🇦 Ukraine", "UA"),
    ("🇦🇪 United Arab Emirates", "AE"),
    ("🇬🇧 United Kingdom", "GB"),
    ("🇺🇸 United States", "US"),
    ("🇺🇾 Uruguay", "UY"),
    ("🇺🇿 Uzbekistan", "UZ"),
    ("🇻🇺 Vanuatu", "VU"),
    ("🇻🇪 Venezuela", "VE"),
    ("🇻🇳 Vietnam", "VN"),
    ("🇾🇪 Yemen", "YE"),
    ("🇿🇲 Zambia", "ZM"),
    ("🇿🇼 Zimbabwe", "ZW"),
]

# Hafta kunlari (ingliz → o'zbek)
WEEKDAYS_UZ = {
    "Monday": "Dushanba",
    "Tuesday": "Seshanba",
    "Wednesday": "Chorshanba",
    "Thursday": "Payshanba",
    "Friday": "Juma",
    "Saturday": "Shanba",
    "Sunday": "Yakshanba",
}

# Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# /start handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = []
    row = []
    for i, (name, code) in enumerate(COUNTRIES):
        row.append(InlineKeyboardButton(name, callback_data=code))
        if (i + 1) % 2 == 0:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🌍 Dunyodagi barcha davlatlardan birini tanlang:", reply_markup=reply_markup)

# Tugma bosilganda
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    country_code = query.data
    country_info = next((item for item in COUNTRIES if item[1] == country_code), None)
    if not country_info:
        await query.edit_message_text("❌ Noma'lum davlat.")
        return

    flag_name = country_info[0]  # "🇺🇿 Uzbekistan"
    country_display = flag_name  # bayroq + nom

    # Hozirgi UTC vaqt (sekundlar bilan)
    now = datetime.now(timezone.utc)
    time_str = now.strftime("%H:%M:%S")
    date_str = now.strftime("%Y-%m-%d")
    weekday_en = now.strftime("%A")
    weekday_uz = WEEKDAYS_UZ.get(weekday_en, weekday_en)

    # Bayramlarni tekshirish
    try:
        if country_code in holidays.list_supported_countries():
            country_holidays = holidays.country_holidays(country_code)
            today_holidays = country_holidays.get(now.date())
            if today_holidays:
                holiday_text = f"🎉 Bayram: {today_holidays}"
            else:
                holiday_text = "❌ Bugun bayram yo'q"
        else:
            holiday_text = "⚠️ Bayram ma'lumotlari mavjud emas"
    except Exception:
        holiday_text = "⚠️ Bayram ma'lumotlari olishda xatolik"

    # Xabar tayyorlash
    message = (
        f"{country_display}\n\n"
        f"🕗 Soat (UTC): {time_str}\n"
        f"📅 Sana: {date_str}\n"
        f"📆 Kun: {weekday_uz}\n"
        f"{holiday_text}"
    )

    await query.edit_message_text(message)

# Asosiy funksiya
def main():
    if BOT_TOKEN == "BU_YERGA_OZINGIZNING_BOT_TOKENINGIZNI_QO'YING":
        raise ValueError("❗ Iltimos, BOT_TOKEN o'zgaruvchisiga o'zingizning bot tokeningizni qo'ying!")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("✅ Bot ishga tushdi! Telegramda /start yozing.")
    app.run_polling()

if __name__ == "__main__":
    main()
