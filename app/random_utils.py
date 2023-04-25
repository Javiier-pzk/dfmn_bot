from random import choice, randint
from telebot import TeleBot
from telebot.types import Message
from app.constants import *

class Decider:

	def __init__(self, bot: TeleBot, chat_id: str):
		self.bot = bot
		self.chat_id = chat_id

	def decide(self):
		sent_message = self.bot.send_message(self.chat_id, OPTIONS_TEXT)
		self.bot.register_next_step_handler(sent_message, self.options_handler)
	
	def options_handler(self, message: Message):
		options = message.text.split(COMMA)
		decision = choice(options)
		self.bot.reply_to(message, DECISION_STR + decision)


class CoinFlipper:

	@staticmethod
	def flip(bot: TeleBot, chat_id: str):
		outcome = choice(COIN_FLIP_CHOICES)
		bot.send_message(chat_id, OUTCOME_STR + outcome)


class RandomNumberGenerator:

	def __init__(self, bot: TeleBot, chat_id: str):
		self.bot = bot
		self.chat_id = chat_id
	
	def generate(self) -> str:
		sent_message = self.bot.send_message(self.chat_id, LOWER_BOUND_TEXT)
		self.bot.register_next_step_handler(sent_message, self.lower_bound_handler)

	def lower_bound_handler(self, message: Message):
		num_str = message.text.strip()
		try:
			lower_bound = int(num_str)
			sent_message = self.bot.send_message(self.chat_id, UPPER_BOUND_TEXT)
			self.bot.register_next_step_handler(
				sent_message, self.upper_bound_handler, lower_bound)
		except ValueError:
			error_message = self.bot.send_message(self.chat_id, INVALID_INT_MESSAGE)
			self.bot.register_next_step_handler(error_message, self.lower_bound_handler)

	def upper_bound_handler(self, message: Message, lower_bound: int):
		num_str = message.text.strip()
		try:
			upper_bound = int(num_str)
			rand_int = randint(lower_bound, upper_bound)
			self.bot.send_message(self.chat_id, RAND_INT_STR + str(rand_int))
		except ValueError:
			error_message = self.bot.send_message(self.chat_id, INVALID_INT_MESSAGE)
			self.bot.register_next_step_handler(
				error_message, self.upper_bound_handler, lower_bound)