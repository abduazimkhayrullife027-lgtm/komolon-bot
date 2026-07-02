from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = "8517214199:AAGgJBpZv7RypTdj5yNYmwLBz3EOO5D6p-s"

keyboard = [
    ["🍽 Menyu", "🛒 Buyurtma"],
    ["📍 Manzil", "📞 Aloqa"]
]

reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

user_data = {}

payment_keyboard = ReplyKeyboardMarkup(
    [["💳 Borganda online tolash", "💵 Naqd"]],
    resize_keyboard=True
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🍽 Komolon Milliy Taomlar botiga xush kelibsiz!",
        reply_markup=reply_markup
    )

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    text = update.message.text

    # MENYU
    if text == "🍽 Menyu":
        await update.message.reply_text(
            "🍛 MENYU:\n\n"
            "Osh - 30 000 so'm\n"
            "Shashlik - 25 000 so'm\n"
            "Somsa - 8 000 so'm"
        )

    # BUYURTMA BOSHLASH
    elif text == "🛒 Buyurtma":
        user_data[user_id] = {}
        await update.message.reply_text("🍛 Qaysi taomni buyurtma qilasiz?")

    # TAOM
    elif user_id in user_data and "food" not in user_data[user_id]:
        user_data[user_id]["food"] = text
        await update.message.reply_text("🔢 Nechta buyurtma qilasiz?")

    # SONI
    elif user_id in user_data and "qty" not in user_data[user_id]:
        user_data[user_id]["qty"] = text
        await update.message.reply_text("📞 Telefon raqamingizni yuboring")

    # TELEFON
    elif user_id in user_data and "phone" not in user_data[user_id]:
        user_data[user_id]["phone"] = text
        await update.message.reply_text("📍 Manzilingizni yozing")

    # MANZIL
    elif user_id in user_data and "address" not in user_data[user_id]:
        user_data[user_id]["address"] = text
        await update.message.reply_text(
            "💳 To‘lov turini tanlang:",
            reply_markup=payment_keyboard
        )

    # TO‘LOV
        user_data[user_id]["payment"] = text

        order = user_data[user_id]

        if text == "💳 Borganda online tolash":
            pay_link = "https://online.borg.uz/"
        else:
            pay_link = "💵 Naqd to‘lov (yetkazilganda)"

        await context.bot.send_message(
            chat_id=user_id,
            text=f"""
🛒 BUYURTMA QABUL QILINDI

🍛 Taom: {order['food']}
🔢 Soni: {order['qty']}
📞 Tel: {order['phone']}
📍 Manzil: {order['address']}
💳 To‘lov: {text}

👉 To‘lov:
{pay_link}

Rahmat! 🍽
"""
        )

        await update.message.reply_text("✅ Buyurtma muvaffaqiyatli yakunlandi!", reply_markup=reply_markup)

        del user_data[user_id]

    elif text == "📍 Manzil":
        await update.message.reply_text("📍 Toshkent, Komolon bozori yonida")

    elif text == "📞 Aloqa":
        await update.message.reply_text("📞 +998 XX XXX XX XX")

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

print("Bot ishga tushdi...")
app.run_polling()