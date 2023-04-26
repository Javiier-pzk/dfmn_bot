import os
import telebot
from threading import Thread
from dotenv import load_dotenv
from app.constants import *
from app.suggester import Recommender
from app.random_utils import *
from flask import Flask, request
from queue import Queue

app = Flask(__name__)

load_dotenv()
BOT_TOKEN = os.getenv(BOT_TOKEN)
WEBHOOK_DOMAIN = os.getenv(WEBHOOK_DOMAIN)
WEBHOOK_URL = WEBHOOK_DOMAIN + BOT_TOKEN
update_queue = Queue()

commands = [telebot.types.BotCommand(SUGGEST_COMMAND, SUGGEST_COMMAND_DESC),
			telebot.types.BotCommand(DECIDE_COMMAND, DECIDE_COMMAND_DESC),
	      	telebot.types.BotCommand(COIN_COMMAND,COIN_COMMAND_DESC),
	        telebot.types.BotCommand(RNG_COMMAND, RNG_COMMAND_DESC),
			telebot.types.BotCommand(DICE_COMMAND, DICE_COMMAND_DESC)]


dfmn_bot = telebot.TeleBot(BOT_TOKEN)
dfmn_bot.set_my_commands(commands)
dfmn_bot.set_my_description(BOT_DESC)
dfmn_bot.remove_webhook()
dfmn_bot.set_webhook(url=WEBHOOK_URL)

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


@app.route('/' + BOT_TOKEN, methods=[POST_REQUEST])
def receive_updates():
    update = telebot.types.Update.de_json(request.stream.read().decode())
    update_queue.put(update)
    return STATUS_OK


def handle_updates(update_queue: Queue):
	while True:
		update = update_queue.get()
		dfmn_bot.process_new_updates([update])
		update_queue.task_done()


update_thread = Thread(target=handle_updates, args=(update_queue,))
update_thread.start()