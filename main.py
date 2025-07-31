import requests
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = "8233163567:AAH3e52dUJBcI7oKwO5iMM5X1CsVHNujmsk"
API_URL = "https://api.cricbuzz.com/cricket-scores/v1/live"

bot = Bot(token=BOT_TOKEN)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    r = requests.get(API_URL)
    data = r.json()

    msg = "🏏 আজকের লাইভ ম্যাচ:\n\n"
    context.user_data['matches'] = {}

    for i, match in enumerate(data.get("matches", []), start=1):
        title = match['matchInfo']['matchDesc']
        teams = match['matchInfo']['team1']['teamName'] + " vs " + match['matchInfo']['team2']['teamName']
        match_id = match['matchInfo']['matchId']
        msg += f"{i}. {teams} ({title})\n"
        context.user_data['matches'][str(i)] = match_id

    msg += "\n👉 যেকোনো নাম্বার দিন (যেমন 1) ম্যাচ ডিটেইলস পেতে।"
    await update.message.reply_text(msg)

async def match_details(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg_id = update.message.text.strip()

    if msg_id not in context.user_data.get('matches', {}):
        await update.message.reply_text("❌ ভুল নাম্বার দিয়েছেন।")
        return

    match_id = context.user_data['matches'][msg_id]
    url = f"https://api.cricbuzz.com/cricket-scores/v1/match/{match_id}"
    res = requests.get(url).json()

    team1 = res['matchInfo']['team1']['teamName']
    team2 = res['matchInfo']['team2']['teamName']
    toss = res.get('matchInfo', {}).get('toss', {}).get('text', 'Toss info not available')
    status = res['matchInfo']['status']
    score = res.get('scoreCard', [{}])[0]
    batting = score.get('batTeamDetails', {}).get('batTeamName', 'N/A')
    total = score.get('scoreDetails', {}).get('runs', 0)
    wickets = score.get('scoreDetails', {}).get('wickets', 0)
    overs = score.get('scoreDetails', {}).get('overs', '0.0')
    fours = score.get('scoreDetails', {}).get('fours', 0)
    sixes = score.get('scoreDetails', {}).get('sixes', 0)

    msg = f"""
🏏 {team1} vs {team2}
🎲 Toss: {toss}
🟢 Currently Batting: {batting}

📊 Score: {total}/{wickets} in {overs} overs
💥 4s: {fours} | 6s: {sixes} | Wickets: {wickets}
📌 Status: {status}
    """
    await update.message.reply_text(msg.strip())

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, match_details))

if __name__ == "__main__":
    app.run_polling()
