import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ✅ তোমার Bot Token
BOT_TOKEN = "8233163567:AAH3e52dUJBcI7oKwO5iMM5X1CsVHNujmsk"

# ✅ Cricket API (public free API)
CRIC_API_URL = "https://api.cricapi.com/v1/currentMatches?apikey=demo&offset=0"

# ✅ লগ সিস্টেম চালু
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# ✅ /start কমান্ড
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 হ্যালো! টাইপ করুন /score লাইভ ক্রিকেট স্কোর পেতে।")

# ✅ /score কমান্ড
async def score(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        response = requests.get(CRIC_API_URL)
        data = response.json()

        if "data" not in data or not data["data"]:
            await update.message.reply_text("⚠️ কোনো লাইভ ম্যাচ পাওয়া যায়নি!")
            return

        message = ""
        for match in data["data"][:3]:  # কেবল ৩টা ম্যাচ দেখানো হবে
            if match.get("status") == "live":
                team1 = match["teams"][0]
                team2 = match["teams"][1]
                score = match["score"]
                message += f"🏏 *{team1} vs {team2}*\n"
                for s in score:
                    message += f"{s['inning']} - {s['r']}/{s['w']} in {s['o']} overs\n"
                message += f"📌 Status: {match['status']}\n\n"
        
        if not message:
            message = "⚠️ কোনো ম্যাচ এখন লাইভ না।"

        await update.message.reply_text(message, parse_mode='Markdown')
    except Exception as e:
        await update.message.reply_text(f"❌ সমস্যা হয়েছে: {e}")

# ✅ অ্যাপ রান করানো
if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("score", score))

    print("✅ Bot is running...")
    app.run_polling()
