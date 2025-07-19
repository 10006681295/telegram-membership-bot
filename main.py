import os
import asyncio
import threading
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Load Environment Variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_LINK = os.getenv("GROUP_LINK")
UPI_ID = os.getenv("UPI_ID")

# Membership Plans
plans = {
    "199": "1 Month Access",
    "299": "2 Months Access",
    "449": "1 Year Access",
    "649": "Lifetime Access"
}

def get_qr_link(amount):
    return f"upi://pay?pa={UPI_ID}&pn=Membership&am={amount}&cu=INR"

# /start Command Handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("✅ /start command received")  # Debug log
    keyboard = [
        [InlineKeyboardButton(f"₹{amt} - {label}", callback_data=amt)]
        for amt, label in plans.items()
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Choose your membership plan:", reply_markup=reply_markup)

# Button Callback Handler
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    amount = query.data
    print(f"✅ User selected ₹{amount}")  # Debug log
    qr = get_qr_link(amount)
    await query.message.reply_text(
        f"Pay ₹{amount} via UPI:\n{qr}\n\nAfter payment, you will receive the group link:\n{GROUP_LINK}"
    )

# Start Telegram Bot
def start_bot():
    async def run():
        app = ApplicationBuilder().token(BOT_TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CallbackQueryHandler(button_callback))
        print("🚀 Bot started...")
        await app.run_polling()

    asyncio.run(run())

# Flask App to keep Render port open
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "✅ Bot is running!"

# Run Flask and Bot Together
if __name__ == '__main__':
    threading.Thread(target=start_bot).start()
    flask_app.run(host="0.0.0.0", port=10000)

