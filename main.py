import os
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# --- PRE-CONFIGURED TOKENS ---
BOT_TOKEN = "8810144336:AAGDZaKMn36qoy8BVKQwVnKwRGFbgyZXP5U"
OMDB_API_KEY = "40c9c3cb"

# ඔයාගේ Channels සහ Groups වල Links
MY_CHANNELS = {
    "LastShip S01 Sub": "https://t.me/lastshipS01subsinhala",
    "Hawk Cinema": "https://telegram.me/hawkcinema",
    "PiratesBay LK": "https://t.me/PiratesBayLK",
    "Channel 4": "https://t.me/Channel4Link",
    "Channel 5": "https://t.me/Channel5Link"
}

def get_film_info(name):
    url = f"http://www.omdbapi.com/?t={name}&apikey={OMDB_API_KEY}"
    r = requests.get(url).json()
    if r.get("Response") == "True":
        return r
    return None

async def search_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message or not message.text:
        return

    film_name = message.text
    status_msg = await message.reply_text(f"🔍 `{film_name}` hoyanawa...")

    info = get_film_info(film_name)
    
    if not info:
        await status_msg.edit_text("❌ Film eka OMDb eke hoyaganna ba. Name eka hari da kiyala balanna.")
        return

    title = info.get('Title')
    imdb_id = info.get('imdbID')
    
    stream_link = f"https://vidsrc.to/embed/movie/{imdb_id}"
    yts_search_link = f"https://yts.mx/browse-movies/{title.replace(' ', '%20')}"
    sinhala_sub_link = f"https://www.baiscope.lk/?s={title.replace(' ', '+')}"

    caption = f"""
🎬 *{title}* ({info.get('Year')})

📅 Release Date: {info.get('Released')}
⭐ IMDB Rating: {info.get('imdbRating')}
📝 Plot: {info.get('Plot')[:250]}...

📍 *Hall Search:*
• Scope: https://scope-cinemas.com/?s={title.replace(' ', '+')}
• BookMyShow: https://lk.bookmyshow.com/explore/movies?q={title.replace(' ', '+')}
"""

    buttons = []
    buttons.append([InlineKeyboardButton("▶️ Direct Watch Online (Instant Stream)", url=stream_link)])
    buttons.append([InlineKeyboardButton("📥 Direct YTS Download / Torrents", url=yts_search_link)])
    buttons.append([InlineKeyboardButton("📝 Sinhala Subtitle Search", url=sinhala_sub_link)])

    for name, link in MY_CHANNELS.items():
        buttons.append([InlineKeyboardButton(f"📂 {name} Telegram Channel", url=link)])

    await status_msg.delete()

    poster_url = info.get('Poster')
    if poster_url and poster_url != "N/A":
        await message.reply_photo(
            photo=poster_url,
            caption=caption,
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    else:
        await message.reply_text(
            text=caption,
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(buttons)
        )

if __name__ == "__main__":
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_handler))
    print("Bot is running...")
    app.run_polling()
