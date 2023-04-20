import os
import telebot
from dotenv import load_dotenv
from Decider import Decider

load_dotenv()

bot_token = os.getenv('BOT_TOKEN')
dfmn_bot = telebot.TeleBot(bot_token)


@dfmn_bot.message_handler(commands=['start'])
def send_welcome(message):
	username = message.from_user.username
	dfmn_bot.reply_to(message, f"Hi {username}, what can I do for you today?")


@dfmn_bot.message_handler(commands=['decide'])
def make_decision(message):
	reply = Decider.choose_options(message.text)
	dfmn_bot.reply_to(message, reply)
	

@dfmn_bot.message_handler(commands=['coinflip'])
def coin_flip(message):
	choice = Decider.coin_flip()
	dfmn_bot.reply_to(message, choice)
	

@dfmn_bot.message_handler(commands=['number'])
def generate_random_number(message):
	reply = Decider.generate_rand_int(message.text)
	dfmn_bot.reply_to(message, reply)


@dfmn_bot.message_handler(func=lambda m: True)
def echo_all(message):
	dfmn_bot.reply_to(message, message.text)
	

dfmn_bot.infinity_polling()