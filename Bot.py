from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from deep_translator import GoogleTranslator
from langdetect import detect
import os

TOKEN = os.getenv("TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "أهلاً بك!\n"
        "أرسل أي نص.\n"
        "إذا كان بالعربية سأترجمه إلى الإنجليزية.\n"
        "إذا كان بالإنجليزية سأترجمه إلى العربية."
    )

async def translate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    try:
        lang = detect(text)

        if lang == "ar":
            translated = GoogleTranslator(source="ar", target="en").translate(text)
            await update.message.reply_text(f"🇬🇧\n{translated}")

        else:
            translated = GoogleTranslator(source="en", target="ar").translate(text)
            await update.message.reply_text(f"🇸🇦\n{translated}")

    except Exception as e:
        await update.message.reply_text(f"حدث خطأ:\n{e}")

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, translate))

print("Bot Started...")
app.run_polling()