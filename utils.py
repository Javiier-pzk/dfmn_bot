START_COMMAND = 'start'
RNG_COMMAND = 'rng'
DECIDE_COMMAND = 'decide'
SUGGEST_COMMAND = 'suggest'
BOT_TOKEN = 'BOT_TOKEN'
COIN_COMMAND = 'coin'
DICE_COMMAND = 'dice'
OPTIONS_TEXT = 'Please input options. Separate multiple options by commas.'
LOWER_BOUND_TEXT = 'Enter lower bound (integer)'
UPPER_BOUND_TEXT = 'Enter upper bound (integer)'
COIN_FLIP_CHOICES = ['heads', 'tails']
COMMA = ','

class TextUtils:

	COMMANDS = """
	➡️ /decide -> Make a random decision
	➡️ /coin -> Flip a coin
	➡️ /rng -> Generate a random number between 2 integers of your choice
	➡️ /dice -> Roll a die
	➡️ /suggest -> Get suggestions on places/restaurants/eateries
	"""

	@staticmethod
	def get_start_message(username: str) -> str:
		return f"""
		Hello @{username}! Here are my list of supported commands.
		{TextUtils.COMMANDS}
		To get started, type any command you see above 🤖.
		"""

	@staticmethod
	def get_unknown_command_message() -> str:
		return f"""
		I'm sorry, I do not understand this command. Here are some commands you can try:
		{TextUtils.COMMANDS}
		"""

	@staticmethod
	def get_invalid_int_message(invalid_int: str) -> str:
		return f'{invalid_int} is not a valid integer. Please try again.'
	
	@staticmethod
	def get_decision_str(decision: str) -> str:
		return f'The decision is: {decision}.'

	@staticmethod
	def get_outcome_str(outcome: str) -> str:
		return f'The outcome is: {outcome}.'
	
	def get_rand_int_str(rand_int: str|int) -> str:
		return f'The random number is: {rand_int}'