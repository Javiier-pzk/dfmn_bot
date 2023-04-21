START_COMMAND = 'start'
RNG_COMMAND = 'rng'
RNG_COMMAND_DESC = 'Generate a random number between 2 integers of your choice'
DECIDE_COMMAND = 'decide'
DECIDE_COMMAND_DESC = 'Make a random decision'
SUGGEST_COMMAND = 'suggest'
SUGGEST_COMMAND_DESC = 'Get suggestions on places/restaurants/eateries'
BOT_TOKEN_VAR_NAME = 'BOT_TOKEN'
COIN_COMMAND = 'coin'
COIN_COMMAND_DESC = 'Flip a coin'
DICE_COMMAND = 'dice'
DICE_COMMAND_DESC = 'Roll a die'
OPTIONS_TEXT = 'Please input options. Separate multiple options by commas.'
LOWER_BOUND_TEXT = 'Enter lower bound (integer)'
UPPER_BOUND_TEXT = 'Enter upper bound (integer)'
COIN_FLIP_CHOICES = ['heads', 'tails']
COMMA = ','
FOOD_TEXT = 'Food'
PLACES_TEXT = 'Places'
CATEGORY_TEXT = 'Please select category'
LOCATION_TEXT = 'Please share your location.'
RADIUS_TEXT = 'Please select search radius'
KM = ' KM'
IS_OPEN_TEXT = 'Do you want to only search for places that are currently open?'
YES_TEXT = 'Yes'
NO_TEXT = 'No'
API_KEY_VAR_NAME = 'API_KEY'
GET_REQUEST = 'GET'
KEY = 'key'
KEYWORD = 'keyword'
LOCATION = 'location'
RADIUS = 'radius'
OPEN_NOW = 'opennow'
DECISION_STR = 'The decision is: '
OUTCOME_STR = 'The outcome is: '
RAND_INT_STR = 'The random number is: '
INVALID_INT_MESSAGE = 'Invalid integer. Please try again.'
COMMANDS = f"""
➡️ /{DECIDE_COMMAND} -> {DECIDE_COMMAND_DESC}
➡️ /{COIN_COMMAND} -> {COIN_COMMAND_DESC}
➡️ /{RNG_COMMAND} -> {RNG_COMMAND_DESC}
➡️ /{DICE_COMMAND} -> {DICE_COMMAND_DESC}
➡️ /{SUGGEST_COMMAND} -> {SUGGEST_COMMAND_DESC}
"""
START_MESSAGE = f"""
Here are some things I can do:
{COMMANDS}
You can find these commands in the menu button below as well!
"""
UNKNOWN_COMMAND_MESSAGE = f"""
I'm sorry, I do not understand this command. Here are some commands you can try:
{COMMANDS}
"""
BOT_DESC = """
Hello 👋, I am tootiebot 🤖! 
Press the start button to see what I can do!
"""