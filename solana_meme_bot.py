import os
import requests
from telegram import Update, ParseMode
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN")
BIRDEYE_API = "https://public-api.birdeye.so/public/tokenlist?sort_by=volume_24h"

async def trending(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔍 Fetching trending Solana meme coins...")

    try:
        response = requests.get(BIRDEYE_API)
        tokens = response.json().get("data", [])[:5]

        msg = "🚀 *Top Meme Coins Solana (24H Volume)*\n\n"
        for i, token in enumerate(tokens, 1):
            symbol = token.get("symbol")
            price = token.get("price_usd", 0)
            volume = token.get("volume_24h", 0)
            address = token.get("address")
            msg += f"*{i}. {symbol}* - ${price:,.4f}\n"
            msg += f"💸 Volume: ${volume:,.0f}\n"
            msg += f"📊 [Chart](https://birdeye.so/token/{address})\n\n"

        await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)

    except Exception as e:
        await update.message.reply_text(f"⚠️ Error fetching data: {e}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("trending", trending))
    print("🤖 Bot is running...")
    app.run_polling()
