import os
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Bot Token from environment variable
BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_LINK = "https://t.me/+Vmo1IluW925hNjE1"

# Flask App (for Render health check)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

# Membership Plans
plans = {
    "199": "1 Month Access",
    "299": "2 Month Access",
    "449": "1 Year Access",
    "649": "Lifetime Access"
}

# Generate UPI QR link
def get_qr_link(amount):
    upi_id = "jaanuragagan@fam"
    return f"upi://pay?pa={upi_id}&pn=Anurag&am={amount}&cu=INR"

# /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        [InlineKeyboardButton(f"₹{amt} - {label}", callback_data=amt)]
        for amt, label in plans.items()
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.message.reply_text("Choose your membership plan:", reply_markup=keyboard)

# Button click callback
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    amount = query.data
    qr_link = get_qr_link(amount)
    await query.message.reply_text(
        f"Pay ₹{amount} via UPI:\n{qr_link}\n\n✅ After successful payment, you’ll receive your access link:\n{GROUP_LINK}"
    )

# Run Telegram Bot
if __name__ == '__main__':
    telegram_app = ApplicationBuilder().token(BOT_TOKEN).build()
    telegram_app.add_handler(CommandHandler("start", start))
    telegram_app.add_handler(CallbackQueryHandler(button_callback))
    telegram_app.run_polling()
    from flask import Flask
import threading

flask_app = Flask(__name__)

@flask_app.route('/')
def index():
    return "Bot is running!"

threading.Thread(target=lambda: flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))).start()

