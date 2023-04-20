import random
from telebot import TeleBot
from telebot.types import Message

class Decider:

	def __init__(self, bot: TeleBot, chat_id: str):
		self.bot = bot
		self.chat_id = chat_id

	def decide(self):
		text = "Please input options. Separate multiple options by commas."
		sent_message = self.bot.send_message(self.chat_id, text)
		self.bot.register_next_step_handler(sent_message, self.options_handler)
	
	def options_handler(self, message: Message):
		options = message.text.split(",")
		weights = [1 / len(options)] * len(options)
		decision = random.choices(options, weights=weights, k=1)
		decision_str = f'The decision is: {decision[0].strip()}.'
		self.bot.reply_to(message, decision_str)


class CoinFlipper:

	@staticmethod
	def flip(bot: TeleBot, chat_id: str):
		choices = ['heads', 'tails']
		weights = [1 / len(choices)] * len(choices)
		outcome = random.choices(choices, weights=weights, k=1)
		outcome_str = f'The outcome is: {outcome[0].strip()}.'
		bot.send_message(chat_id, outcome_str)


class RandomNumberGenerator:

	def __init__(self, bot: TeleBot, chat_id: str):
		self.bot = bot
		self.chat_id = chat_id
	
	def generate(self) -> str:
		text = 'Enter lower bound (integer)'
		sent_message = self.bot.send_message(self.chat_id, text)
		self.bot.register_next_step_handler(sent_message, self.lower_bound_handler)

	def lower_bound_handler(self, message: Message):
		num_str = message.text.strip()
		try:
			lower_bound = int(num_str)
			text = 'Enter upper bound (integer)'
			sent_message = self.bot.send_message(self.chat_id, text)
			self.bot.register_next_step_handler(
				sent_message, self.upper_bound_handler, lower_bound)
		except ValueError:
			text = f'{num_str} is not a valid integer. Please try again.'
			error_message = self.bot.send_message(self.chat_id, text)
			self.bot.register_next_step_handler(error_message, self.lower_bound_handler)

	def upper_bound_handler(self, message: Message, lower_bound: int):
		num_str = message.text.strip()
		try:
			upper_bound = int(num_str)
			rand_int = random.randint(lower_bound, upper_bound)
			rand_int_str = f"The random number is: {rand_int}"
			self.bot.send_message(self.chat_id, rand_int_str)
		except ValueError:
			text = f'{num_str} is not a valid integer. Please try again.'
			error_message = self.bot.send_message(self.chat_id, text)
			self.bot.register_next_step_handler(
				error_message, self.upper_bound_handler, lower_bound)