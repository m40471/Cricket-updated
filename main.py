import logging
import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler
)

# ▶️ টেলিগ্রাম বট টোকেন
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_TOKEN_HERE")

# ✅ লগিং সিস্টেম (ডিবাগিং এর জন্য ভালো)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# 📌 /start কমান্ড হ্যান্ডলার
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 হ্যালো! আমি সফলভাবে চালু হয়েছি!")

# 📌 /help কমান্ড হ্যান্ডলার
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 আমি Telegram বট! শুধু /start লিখে শুরু করুন।")

# ▶️ অ্যাপ্লিকেশন তৈরি ও হ্যান্ডলার যুক্ত করা
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))

# ▶️ বট চালু (24x7 polling mode)
if __name__ == "__main__":
    print("✅ Bot is running...")
    app.run_polling()
