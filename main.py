
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_LINK = "https://t.me/+Vmo1IluW925hNjE1"

plans = {
    "199": "1 Month Access",
    "299": "2 Month Access",
    "449": "1 Year Access",
    "649": "Lifetime Access"
}

def get_qr_link(amount):
    upi_id = "jaanuragagan@fam"
    return f"https://upi.io/pay?pa={upi_id}&pn=Membership&am={amount}&cu=INR"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        [InlineKeyboardButton(f"₹{amt} - {label}", callback_data=amt)]
        for amt, label in plans.items()
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.message.reply_text("Choose your membership plan:", reply_markup=keyboard)

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    amount = query.data
    qr_link = get_qr_link(amount)
    await query.message.reply_text(f"Pay ₹{amount} via UPI:\nupi://pay?pa=jaanuragagan@fam&pn=Anurag&am={amount}&cu=INR")





if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_callback))
    print("Bot started...")
    app.run_polling()
@bot.callback_query_handler(func=lambda call: True)
async def handle_callback_query(call):
    amount = 199
    qr_link = await generate_qr(amount)

    await call.message.reply_text(
        f"Pay ₹{amount} via UPI:\n{qr_link}\n\nAfter successful payment, your access link:\n{GROUP_LINK}"
    )

