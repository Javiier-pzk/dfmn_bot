import os
import telebot
import time
from dotenv import load_dotenv
from constants import *
from suggester import Recommender
from random_utils import *
from flask import Flask, request

app = Flask(__name__)

load_dotenv()
BOT_TOKEN = os.getenv(BOT_TOKEN_VAR_NAME)
PORT = os.getenv(PORT)
WEBHOOK_URL = 'https://dfmn-bot.herokuapp.com/' + BOT_TOKEN

commands = [telebot.types.BotCommand(SUGGEST_COMMAND, SUGGEST_COMMAND_DESC),
			telebot.types.BotCommand(DECIDE_COMMAND, DECIDE_COMMAND_DESC),
	      	telebot.types.BotCommand(COIN_COMMAND,COIN_COMMAND_DESC),
	        telebot.types.BotCommand(RNG_COMMAND, RNG_COMMAND_DESC),
			telebot.types.BotCommand(DICE_COMMAND, DICE_COMMAND_DESC)]


dfmn_bot = telebot.TeleBot(BOT_TOKEN)
dfmn_bot.set_my_commands(commands)
dfmn_bot.set_my_description(BOT_DESC)
dfmn_bot.set_webhook(url=WEBHOOK_URL)


@app.route('/' + BOT_TOKEN, methods=[POST_REQUEST])
def handle_updates():
    update = telebot.types.Update.de_json(request.stream.read().decode())
    dfmn_bot.process_new_updates([update])
    time.sleep(0.1)


@dfmn_bot.message_handler(commands=[START_COMMAND])
def send_start_message(message):
	dfmn_bot.send_message(message.chat.id, START_MESSAGE)


@dfmn_bot.message_handler(commands=[DECIDE_COMMAND])
def make_decision(message):
	Decider(dfmn_bot, message.chat.id).decide()
	

@dfmn_bot.message_handler(commands=[COIN_COMMAND])
def flip_coin(message):
	CoinFlipper.flip(dfmn_bot, message.chat.id)
	

@dfmn_bot.message_handler(commands=[RNG_COMMAND])
def generate_random_number(message):
	RandomNumberGenerator(dfmn_bot, message.chat.id).generate()


@dfmn_bot.message_handler(commands=[DICE_COMMAND])
def send_dice(message):
	dfmn_bot.send_dice(message.chat.id)


@dfmn_bot.message_handler(commands=[SUGGEST_COMMAND])
def suggest(message):
	Recommender(dfmn_bot, message.chat.id).recommend()
		

@dfmn_bot.message_handler(func=lambda m: True)
def echo_all(message):
	dfmn_bot.reply_to(message, UNKNOWN_COMMAND_MESSAGE)


dfmn_bot.run_webhooks(port=PORT, url_path=BOT_TOKEN)


if __name__ == '__main__':
	app.run(host='127.0.0.1', port=PORT)
