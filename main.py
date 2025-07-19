import os
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import asyncio

# Bot Token and Group Link from environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_LINK = os.getenv("GROUP_LINK")
UPI_ID = os.getenv("UPI_ID")

plans = {
    "199": "1 Month Access",
    "299": "2 Months Access",
    "449": "1 Year Access",
    "649": "Lifetime Access"
}

def get_qr_link(amount):
    return f"upi://pay?pa={UPI_ID}&pn=Membership&am={amount}&cu=INR"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(f"₹{amt} - {label}", callback_data=amt)] for amt, label in plans.items()]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Choose your membership plan:", reply_markup=reply_markup)

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    amount = query.data
    qr = get_qr_link(amount)
    await query.answer()
    await query.message.reply_text(
        f"Pay ₹{amount} via UPI:\n{qr}\n\nAfter payment, you will receive the group link:\n{GROUP_LINK}"
    )

# Flask App to keep Render port open
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

async def run_bot():
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_callback))
    print("Bot started...")
    await application.run_polling()

def start_async_loop():
    loop = asyncio.get_event_loop()
    loop.create_task(run_bot())

if __name__ == "__main__":
    start_async_loop()
    app.run(host="0.0.0.0", port=10000)


