import os import logging import requests from flask import Flask, request, send_from_directory from telegram import Update from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

Fetch environment variables

TOKEN = os.getenv("TOKEN") BASE_URL = os.getenv("BASE_URL") UPLOAD_FOLDER = "uploads"

Ensure upload directory exists

if not os.path.exists(UPLOAD_FOLDER): os.makedirs(UPLOAD_FOLDER)

app = Flask(name) logging.basicConfig(level=logging.INFO)

def start(update: Update, context: CallbackContext) -> None: update.message.reply_text("Send me a .json or .php file to host.")

def handle_document(update: Update, context: CallbackContext) -> None: file = update.message.document file_ext = file.file_name.split(".")[-1]

if file_ext not in ["json", "php"]:
    update.message.reply_text("Only .json and .php files are allowed.")
    return

file_path = os.path.join(UPLOAD_FOLDER, file.file_name)
file = context.bot.get_file(file.file_id)
file.download(file_path)

# Generate hosted file link
file_url = f"{BASE_URL}/files/{file.file_name}"
update.message.reply_text(f"✅ Your file is hosted at: {file_url}")

@app.route("/files/<filename>") def serve_file(filename): return send_from_directory(UPLOAD_FOLDER, filename)

def main(): updater = Updater(TOKEN) dp = updater.dispatcher dp.add_handler(CommandHandler("start", start)) dp.add_handler(MessageHandler(Filters.document, handle_document)) updater.start_polling() updater.idle()

if name == "main": main() app.run(host="0.0.0.0", port=10000)