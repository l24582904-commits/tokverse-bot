import os
import json
import asyncio
import logging
from http.server import BaseHTTPRequestHandler

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = os.environ.get("8977664827:AAGTUytpAg4gPl7xsmxBQN2U-pZehBaqRTk", "")

logging.basicConfig(level=logging.INFO)
application = Application.builder().token(TOKEN).updater(None).build()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام مشتی! 🔥\nربات AI TOK آماده است.\nپیامت رو بفرست."
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "پیامت رسید مشتی! برای فعال‌شدن هوش مصنوعی، باید اتصال سرویس AI رو هم تنظیم کنیم."
    )


application.add_handler(CommandHandler("start", start))
application.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
)


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", 0))
            data = json.loads(self.rfile.read(length))
            update = Update.de_json(data, application.bot)

            async def process():
                async with application:
                    await application.process_update(update)

            asyncio.run(process())

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")
        except Exception:
            logging.exception("Webhook error")
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b"ERROR")

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"AI TOK BOT is running")
