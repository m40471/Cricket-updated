import logging
import aiohttp
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = "8233163567:AAH3e52dUJBcI7oKwO5iMM5X1CsVHNujmsk"
API_KEY = "3fe5ae0f-e183-44ce-b878-870ec56be11f"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def get_cricket_score():
    url = f"https://api.cricapi.com/v1/currentMatches?apikey={API_KEY}&offset=0"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()

            # শুধু লাইভ ম্যাচগুলো নেবে
            matches = [m for m in data.get("data", []) if "Live" in m.get("status", "")]
            if not matches:
                return "❌ এখন কোনো লাইভ ম্যাচ নেই।"

            result = ""
            for match in matches[:3]:  # প্রথম ৩টি লাইভ ম্যাচ
                team1 = match['teams'][0]
                team2 = match['teams'][1]
                status = match.get("status", "No status")

                score = match.get("score", [])
                if score:
                    team1_score = f"{score[0]['r']} / {score[0]['w']} in {score[0]['o']} overs" if len(score) > 0 else "N/A"
                    team2_score = f"{score[1]['r']} / {score[1]['w']} in {score[1]['o']} overs" if len(score) > 1 else "N/A"
                else:
                    team1_score = team2_score = "স্কোর আপডেট নেই"

                result += f"🏏 {team1} vs {team2}\n📊 {team1}: {team1_score}\n📊 {team2}: {team2_score}\n📢 অবস্থা: {status}\n\n"

            return result.strip()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 হ্যালো! স্কোর জানতে /score কমান্ড দিন।")

async def score(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = await get_cricket_score()
    await update.message.reply_text(msg)

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("score", score))
    app.run_polling()
