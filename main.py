from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# তোমার বট টোকেন এখানে বসানো হয়েছে
BOT_TOKEN = "8233163567:AAH3e52dUJBcI7oKwO5iMM5X1CsVHNujmsk"

# /start কমান্ড হ্যান্ডলার
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 হ্যালো! আমি Render-এ হোস্ট করা একটি লাইভ স্কোর বট!")

# সাধারণ মেসেজ হ্যান্ডলার (পরীক্ষামূলক)
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"⚽ আপনি লিখেছেন: {update.message.text}")

# এন্ট্রি পয়েন্ট
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    app.run_polling()
