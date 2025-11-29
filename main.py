import logging
import os
from datetime import datetime, timezone
import holidays
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, Command handler, CallbackQueryHandler, ContextTypes

# 🔑 Bot tokenini muhit o'zgaruvchisidan olish (Railway daqt sozlanadi)
BOT_TOKEN = ("8496446032:AAF6Yxv7dnrp_qMDXegWVddgrvMQKK3q2uo")
if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN muhit o'zgaruvchisi set qilinmagan! Railway yoki .env faylida belgilang.")

# 🌍 195+ DAVLAT
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

# 🗳️ Prezidentlar (2025-yil noyabr holatiga)
PRESIDENTS = {
    "US": ("Joe Biden", "2021-01-20"),
    "UZ": ("Shavkat Mirziyoyev", "2016-12-14"),
    "RU": ("Vladimir Putin", "2012-05-07"),
    "CN": ("Xi Jinping", "2013-03-15"),
    "FR": ("Emmanuel Macron", "2017-05-14"),
    "DE": ("Frank-Walter Steinmeier", "2017-03-19"),
    "GB": ("Charles III", "2022-09-08"),
    "IN": ("Droupadi Murmu", "2022-07-25"),
    "BR": ("Luiz Inácio Lula da Silva", "2023-01-01"),
    "JP": ("Fumio Kishida", "2021-10-04"),
    "CA": ("Mary Simon", "2021-07-26"),
    "AU": ("David Hurley", "2019-07-01"),
    "TR": ("Recep Tayyip Erdoğan", "2014-08-28"),
    "SA": ("Salman bin Abdulaziz", "2015-01-23"),
    "AE": ("Mohamed bin Zayed Al Nahyan", "2022-05-14"),
    "EG": ("Abdel Fattah el-Sisi", "2014-06-08"),
    "ZA": ("Cyril Ramaphosa", "2018-02-15"),
    "NG": ("Bola Tinubu", "2023-05-29"),
    "KE": ("William Ruto", "2022-09-13"),
    "IL": ("Isaac Herzog", "2021-07-07"),
    "IR": ("Masoud Pezeshkian", "2024-07-30"),
    "PK": ("Asif Ali Zardari", "2024-03-10"),
    "ID": ("Joko Widodo", "2014-10-20"),
    "KR": ("Yoon Suk-yeol", "2022-05-10"),
    "IT": ("Sergio Mattarella", "2015-02-03"),
    "ES": ("Pedro Sánchez", "2018-06-02"),
    "UA": ("Volodymyr Zelenskyy", "2019-05-20"),
    "BY": ("Alexander Lukashenko", "1994-07-20"),
    "KZ": ("Kassym-Jomart Tokayev", "2019-03-20"),
    "MM": ("Min Aung Hlaing", "2021-08-01"),
    "VN": ("To Lam", "2024-10-21"),
    "TH": ("Srettha Thavisin", "2023-08-22"),
    "PH": ("Bongbong Marcos", "2022-06-30"),
    "MY": ("Sultan Ibrahim Iskandar", "2024-01-31"),
    "SG": ("Tharman Shanmugaratnam", "2023-09-14"),
    "NZ": ("Cindy Kiro", "2021-10-21"),
    "SE": ("Ulf Kristersson", "2022-10-18"),
    "NO": ("Jonas Gahr Støre", "2021-10-14"),
    "CH": ("Viola Amherd", "2024-01-01"),
    "PS": ("Mahmoud Abbas", "2005-01-15"),
    "VA": ("Pope Francis", "2013-03-13"),
}

WEEKDAYS_UZ = {
    "Monday": "Dushanba",
    "Tuesday": "Seshanba",
    "Wednesday": "Chorshanba",
    "Thursday": "Payshanba",
    "Friday": "Juma",
    "Saturday": "Shanba",
    "Sunday": "Yakshanba",
}

def format_date_uz(date_str):
    if not date_str:
        return "Noma'lum"
    try:
        d = datetime.strptime(date_str, "%Y-%m-%d")
        months_uz = ["", "Yanvar", "Fevral", "Mart", "Aprel", "May", "Iyun",
                     "Iyul", "Avgust", "Sentabr", "Oktabr", "Noyabr", "Dekabr"]
        return f"{d.day}-{months_uz[d.month]} {d.year} yil"
    except Exception:
        return "Noma'lum"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

ITEMS_PER_PAGE = 10

def build_country_keyboard(page: int = 0):
    start = page * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE
    page_countries = COUNTRIES[start:end]

    keyboard = []
    for name, code in page_countries:
        keyboard.append([InlineKeyboardButton(name, callback_data=f"country:{code}")])

    nav_row = []
    if page > 0:
        nav_row.append(InlineKeyboardButton("⬅️ Oldingi", callback_data=f"page:{page-1}"))
    if end < len(COUNTRIES):
        nav_row.append(InlineKeyboardButton("Keyingi ➡️", callback_data=f"page:{page+1}"))
    if nav_row:
        keyboard.append(nav_row)

    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_markup = build_country_keyboard(page=0)
    await update.message.reply_text("🌍 Davlatlardan birini tanlang (sahifalangan):", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data.startswith("page:"):
        page = int(data.split(":")[1])
        reply_markup = build_country_keyboard(page=page)
        await query.edit_message_text("🌍 Davlatlardan birini tanlang (sahifalangan):", reply_markup=reply_markup)

    elif data.startswith("country:"):
        country_code = data.split(":")[1]
        country_info = next((item for item in COUNTRIES if item[1] == country_code), None)
        if not country_info:
            await query.edit_message_text("❌ Noma'lum davlat.")
            return

        flag_name = country_info[0]
        now = datetime.now(timezone.utc)
        time_str = now.strftime("%H:%M:%S")
        date_str = now.strftime("%Y-%m-%d")
        weekday_uz = WEEKDAYS_UZ.get(now.strftime("%A"), now.strftime("%A"))

        # Bayram ma'lumotini xavfsiz olish
        holiday_text = "⚠️ Bayram ma'lumotlari mavjud emas"
        try:
            if country_code in holidays.list_supported_countries():
                if country_code == "XK":
                    holiday_text = "⚠️ Kosovo uchun bayram ma'lumotlari yo'q"
                else:
                    country_holidays = holidays.country_holidays(country_code)
                    today_holidays = country_holidays.get(now.date())
                    holiday_text = f"🎉 Bayram: {today_holidays}" if today_holidays else "❌ Bugun bayram yo'q"
        except Exception:
            holiday_text = "⚠️ Bayram ma'lumotlarini olishda xatolik"

        # Prezident
        prez_name, prez_since = PRESIDENTS.get(country_code, ("❌ Ma'lumot yo'q", None))
        if prez_since:
            since_text = format_date_uz(prez_since)
            prez_text = f"👤 Bosh rahbar: {prez_name}\n📅 Lavozimga kirgan: {since_text}"
        else:
            prez_text = f"👤 Bosh rahbar: {prez_name}"

        message = (
            f"{flag_name}\n\n"
            f"🕗 Soat (UTC): {time_str}\n"
            f"📅 Sana: {date_str}\n"
            f"📆 Kun: {weekday_uz}\n"
            f"{holiday_text}\n\n"
            f"{prez_text}"
        )
        await query.edit_message_text(message)

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    logging.info("✅ Bot ishga tushdi! Railwayda ishlayapti.")
    app.run_polling()

if __name__ == "__main__":
    main()
