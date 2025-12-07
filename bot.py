import logging, os, requests, base64
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from io import BytesIO

logging.basicConfig(level=logging.INFO)

API_KEY = os.getenv("NOVITA_API_KEY")
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot aktif! Prompt yaz, NSFW resim gelsin 🚀")

async def generate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = update.message.text.strip()
    if not prompt:
        await update.message.reply_text("Prompt yaz knk!")
        return

    await update.message.reply_chat_action("upload_photo")

    url = "https://api.novita.ai/v3/text2img"
    payload = {
        "prompt": prompt + ", masterpiece, best quality, ultra detailed, nsfw, uncensored",
        "negative_prompt": "low quality, blurry, censored, deformed",
        "width": 512,
        "height": 768,
        "steps": 28,
        "sampler_name": "Euler a",
        "cfg_scale": 7
    }
    headers = {"Authorization": f"Bearer {API_KEY}"}

    try:
        r = requests.post(url, json=payload, headers=headers, timeout=180)
        r.raise_for_status()
        img_b64 = r.json()["images"][0]
        img_data = base64.b64decode(img_b64)
        await update.message.reply_photo(photo=img_data, caption="İşte knk 💦")
    except Exception as e:
        await update.message.reply_text(f"Hata: {str(e)}")

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate))
app.run_polling()
