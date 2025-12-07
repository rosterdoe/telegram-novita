import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests
import os
import base64
from io import BytesIO

logging.basicConfig(level=logging.INFO)

NOVITA_KEY = os.getenv("NOVITA_API_KEY")
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("NSFW Bot hazır! Prompt yaz, resim üretelim 🚀")

async def generate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = update.message.text
    await update.message.reply_chat_action("upload_photo")

    url = "https://api.novita.ai/v3/text2img"
    payload = {
        "prompt": prompt + ", masterpiece, best quality, ultra detailed, nsfw, uncensored",
        "negative_prompt": "low, blurry, low quality, censored",
        "width": 512,
        "height": 768,
        "steps": 28,
        "sampler_name": "Euler a",
        "cfg_scale": 7,
        "seed": -1,
        "batch_size": 1
    }
headers = {"Authorization": f"Bearer {NOVITA_API_KEY}"}

    try:
            r = requests.post(url, json=payload, headers=headers, timeout=180)
            r.raise_for_status()
            img_b64 = r.json()["images"][0]
            img_data = base64.b64decode(img_b64)
            await update.message.reply_photo(img_data, caption=prompt[:100])
       except Exception as e:
           await update.message.reply_text(f"Hata: {e}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate))
    app.run_polling()

if __name__ == "__main__":
    main()
