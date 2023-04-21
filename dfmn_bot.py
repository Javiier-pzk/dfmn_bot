import os
import telebot
from dotenv import load_dotenv
from random_utils import *
from utils import *

load_dotenv()

dfmn_bot = telebot.TeleBot(os.getenv(BOT_TOKEN))

@dfmn_bot.message_handler(commands=[START_COMMAND])
def make_decision(message):
	username = message.chat.username
	dfmn_bot.send_message(message.chat.id, TextUtils.get_start_message(username))


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


@dfmn_bot.message_handler(commands=['location'])
def get_location(message):
	sent_message = dfmn_bot.send_message(message.chat.id, "Please share your location.")
	dfmn_bot.register_next_step_handler(sent_message, handle_location)
	

def handle_location(message):
	chat_id = message.chat.id
	location = message.location
	latitude = location.latitude
	longitude = location.longitude
	dfmn_bot.send_message(chat_id, f"Your location is: ({latitude}, {longitude})")
		

@dfmn_bot.message_handler(func=lambda m: True)
def echo_all(message):
	dfmn_bot.reply_to(message, TextUtils.get_unknown_command_message())
	

dfmn_bot.infinity_polling()