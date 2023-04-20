import os
import telebot
from dotenv import load_dotenv
from random_utils import *

load_dotenv()

bot_token = os.getenv('BOT_TOKEN')
dfmn_bot = telebot.TeleBot(bot_token)


@dfmn_bot.message_handler(commands=['start'])
def send_welcome(message):
	username = message.from_user.username
	dfmn_bot.reply_to(message, f"Hi {username}, what can I do for you today?")


@dfmn_bot.message_handler(commands=['decide'])
def make_decision(message):
	Decider(dfmn_bot, message.chat.id).decide()
	
	

@dfmn_bot.message_handler(commands=['coin'])
def coin_flip(message):
	CoinFlipper.flip(dfmn_bot, message.chat.id)
	


@dfmn_bot.message_handler(commands=['number'])
def generate_random_number(message):
	RandomNumberGenerator(dfmn_bot, message.chat.id).generate()



@dfmn_bot.message_handler(commands=['dice'])
def send_dice(message):
	dfmn_bot.send_dice(message.chat.id)

		

@dfmn_bot.message_handler(func=lambda m: True)
def echo_all(message):
	dfmn_bot.reply_to(message, message.text)
	

dfmn_bot.infinity_polling()