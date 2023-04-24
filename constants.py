START_COMMAND = 'start'
RNG_COMMAND = 'rng'
RNG_COMMAND_DESC = 'Generate a random number between 2 integers of your choice.'
DECIDE_COMMAND = 'decide'
DECIDE_COMMAND_DESC = 'Make a random decision.'
SUGGEST_COMMAND = 'suggest'
SUGGEST_COMMAND_DESC = 'Get suggestions on food/malls/entertainment etc.'
BOT_TOKEN_VAR_NAME = 'BOT_TOKEN'
COIN_COMMAND = 'coin'
COIN_COMMAND_DESC = 'Flip a coin.'
DICE_COMMAND = 'dice'
DICE_COMMAND_DESC = 'Roll a die.'
OPTIONS_TEXT = 'Please input options. Separate multiple options by commas.'
LOWER_BOUND_TEXT = 'Enter lower bound (integer)'
UPPER_BOUND_TEXT = 'Enter upper bound (integer)'
COIN_FLIP_CHOICES = ['heads', 'tails']
COMMA = ','
FOOD_TEXT = 'Food'
RESTAURANTS_TEXT = 'Restaurants'
COFFEE_SHOPS_TEXT = 'Coffee shops'
HAWKER_CENTRES_TEXT = 'Hawker centres'
PARKS_TEXT = 'Parks and nature reserves'
FITNESS_AREAS = 'Fitness areas'
PLACES_TEXT = 'Places'
COFFEE_TEXT = 'Coffee'
MALLS_TEXT = 'Shopping malls'
ENTERTAINMENT_TEXT = 'Entertainment'
TOURIST_ATTRACTIONS_TEXT = 'Tourist attractions'

CATEGORY_TEXT = "Please select a suggested category below or enter in your own category. For example, 'Indian Food'"
LOCATION_TEXT = 'Please share your location.'
RADIUS_TEXT = 'Please select search radius'
KM = ' km'
ONLY_OPEN_TEXT = 'Do you want to only search for places that are currently open?'
YES_TEXT = 'Yes'
NO_TEXT = 'No'
API_KEY_VAR_NAME = 'API_KEY'
GET_REQUEST = 'GET'
POST_REQUEST = 'POST'
KEY = 'key'
KEYWORD = 'keyword'
LOCATION = 'location'
RADIUS = 'radius'
OPEN_NOW = 'opennow'
DECISION_STR = 'The decision is: '
OUTCOME_STR = 'The outcome is: '
RAND_INT_STR = 'The random number is: '
INVALID_INT_MESSAGE = 'Invalid integer. Please try again.'
RESULTS_KEY = 'results'
RATING_KEY = 'rating'
NAME_KEY = 'name'
USER_RATINGS_TOTAL_KEY = 'user_ratings_total'
PRICE_LEVEL_KEY = 'price_level'
OPEN_NOW_KEY = 'open_now'
OPENING_HOURS_KEY = 'opening_hours'
GEOMETRY_KEY = 'geometry'
LAT_KEY = 'lat'
LNG_KEY = 'lng'
PHOTOS_KEY = 'photos'
PHOTO_REF = 'photo_reference'
HEIGHT = 'height'
WIDTH = 'width'
MAX_HEIGHT = 'maxheight'
MAX_WIDTH = 'maxwidth'
NUM_REC_MESSAGE = 'How many recommendations do you want to see?'
ZERO_RECOMMENDATIONS_MESSAGE = 'Sorry, I am unable to find any recommendations that fit your criteria 😕'
RECOMMENDATIONS_MESSAGE = "Here are the top {num_rec} {category} recommendations near you:"
PLACE_ID_KEY = 'place_id'
VICINITY_KEY = 'vicinity'
BUSINESS_STATUS_KEY = 'business_status'
OPERATIONAL = 'OPERATIONAL'
INVALID_CATEGORY_MESSAGE = 'Invalid category. Please try again.'
INVALID_LOCATION_MESSAGE = 'Invalid location. Please try again.'
INVALID_RADIUS_MESSAGE = 'Invalid search radius. Please try again.'
INVALID_ONLY_OPEN_MESSAGE = 'Invalid input. Please try again.'
DOLLAR_SIGN = '$'
PICK_RANDOM_RECOMMENDATIONS_MESSAGE = 'Do you want me to pick a random option for you?'
PICK_FOR_ME_TEXT = "Yes, pick for me!"
PICK_MYSELF_TEXT = "No, I'll pick myself!"
BOT_RECOMMENDATION_MESSAGE = 'My recommendation is:'
SIGN_OFF_TEXT = 'Alright! Have a nice day 👋'
COMMANDS = f"""
➡️ /{SUGGEST_COMMAND} -> {SUGGEST_COMMAND_DESC}
➡️ /{DECIDE_COMMAND} -> {DECIDE_COMMAND_DESC}
➡️ /{COIN_COMMAND} -> {COIN_COMMAND_DESC}
➡️ /{RNG_COMMAND} -> {RNG_COMMAND_DESC}
➡️ /{DICE_COMMAND} -> {DICE_COMMAND_DESC}
"""
RECOMMENDATIONS_TEXT = """
Rating: {rating}
Total user ratings: {user_ratings_total}
Price level: {price_level}
Open now: {open_now}
"""
PLACE_NAME = '{index}. {name}'
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
