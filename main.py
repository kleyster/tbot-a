from fastapi import FastAPI
import logging
import telebot
import uvicorn
from config import *

app = FastAPI()

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)
bot = telebot.TeleBot(API_TOKEN)


@app.post(f"/{API_TOKEN}/")
def process_webhook(update: dict):
    if update:
        update = telebot.types.Update.de_json(update)
        bot.process_new_updates([update])
    else:
        return {}


@bot.message_handler(commands=["help", "start"])
async def start_function(message):
    bot.reply_to(message, "HELLO GUEST SEND ME YOUR LOGIN AND PASSWORD")


@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    bot.reply_to(message, message.text)


bot.remove_webhook()

bot.set_webhook(url=WEBHOOK_URL_BASE+WEBHOOK_URL_PATH, certificate=open(WEBHOOK_SSL_CERT, 'r'))


uvicorn.run(app, host=WEBHOOK_LISTEN, port=WEBHOOK_PORT,ssl_certfile=WEBHOOK_SSL_CERT, ssl_keyfile=WEBHOOK_SSL_PRIV)
