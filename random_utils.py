import random
from telebot import TeleBot
from telebot.types import Message
from utils import *

class Decider:

	def __init__(self, bot: TeleBot, chat_id: str):
		self.bot = bot
		self.chat_id = chat_id

	def decide(self):
		sent_message = self.bot.send_message(self.chat_id, OPTIONS_TEXT)
		self.bot.register_next_step_handler(sent_message, self.options_handler)
	
	def options_handler(self, message: Message):
		options = message.text.split(COMMA)
		weights = [1 / len(options)] * len(options)
		decision = random.choices(options, weights=weights, k=1)
		self.bot.reply_to(message, TextUtils.get_decision_str(decision[0].strip()))


class CoinFlipper:

	@staticmethod
	def flip(bot: TeleBot, chat_id: str):
		choices = COIN_FLIP_CHOICES
		weights = [1 / len(choices)] * len(choices)
		outcome = random.choices(choices, weights=weights, k=1)
		bot.send_message(chat_id, TextUtils.get_outcome_str(outcome[0].strip()))


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
			error_message = self.bot.send_message(self.chat_id, 
					TextUtils.get_invalid_int_message(num_str))
			self.bot.register_next_step_handler(error_message, self.lower_bound_handler)

	def upper_bound_handler(self, message: Message, lower_bound: int):
		num_str = message.text.strip()
		try:
			upper_bound = int(num_str)
			rand_int = random.randint(lower_bound, upper_bound)
			self.bot.send_message(self.chat_id, TextUtils.get_rand_int_str(rand_int))
		except ValueError:
			error_message = self.bot.send_message(self.chat_id,
					TextUtils.get_invalid_int_message(num_str))
			self.bot.register_next_step_handler(
				error_message, self.upper_bound_handler, lower_bound)