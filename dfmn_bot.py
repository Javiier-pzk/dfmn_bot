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
	text = "Please input at least 1 option or multiple options separated by commas"
	sent_message = dfmn_bot.reply_to(message, text)
	dfmn_bot.register_next_step_handler(sent_message, options_handler)
	

def options_handler(message):
	options = message.text
	decision = Decider.choose_options(options)
	dfmn_bot.reply_to(message, decision)
	

@dfmn_bot.message_handler(commands=['coinflip'])
def coin_flip(message):
	choice = Decider.coin_flip()
	dfmn_bot.reply_to(message, choice)
	

@dfmn_bot.message_handler(commands=['number'])
def generate_random_number(message):
	text = 'Enter lower bound'
	sent_message = dfmn_bot.send_message(message.chat.id, text)
	dfmn_bot.register_next_step_handler(sent_message, lower_bound_handler)
		

def lower_bound_handler(message):
	num_str = message.text.strip()
	try:
		lower_bound = int(num_str)
		text = 'Enter upper bound'
		sent_message = dfmn_bot.send_message(message.chat.id, text)
		dfmn_bot.register_next_step_handler(sent_message, upper_bound_handler, lower_bound)
	except ValueError:
		text = f'{num_str} is not a valid integer. Please try again'
		dfmn_bot.send_message(message.chat.id, text)
	

def upper_bound_handler(message, lower_bound):
	num_str = message.text.strip()
	try:
		upper_bound = int(num_str)
		rand_int_str = Decider.generate_rand_int(lower_bound, upper_bound)
		dfmn_bot.send_message(message.chat.id, rand_int_str)
	except ValueError:
		text = f'{num_str} is not a valid integer. Please try again'
		dfmn_bot.send_message(message.chat.id, text)
		dfmn_bot.register_next_step_handler(message, lower_bound_handler)


@dfmn_bot.message_handler(commands=['dice'])
def send_dice(message):
	dfmn_bot.send_dice(message.chat.id)

		

@dfmn_bot.message_handler(func=lambda m: True)
def echo_all(message):
	dfmn_bot.reply_to(message, message.text)
	

dfmn_bot.infinity_polling()