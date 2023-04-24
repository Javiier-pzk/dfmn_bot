from telebot import TeleBot
from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InputMediaPhoto, InlineKeyboardButton, InlineKeyboardMarkup
from app.constants import *
import os
import requests
from PIL import Image
from io import BytesIO
from random import randint

class Recommender:
	
	NEARBY_PLACES_URL = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
	PLACES_URL = 'https://maps.googleapis.com/maps/api/place/photo'

	def __init__(self, bot:TeleBot, chat_id: str):
		self.bot = bot
		self.chat_id = chat_id
		self.category = None
		self.latitude = None
		self.longitude = None
		self.radius = None
		self.only_open = False
		self.num_rec = None
		self.api_key = os.getenv(API_KEY_VAR_NAME)
	

	def recommend(self):
		keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
		categories = [FOOD_TEXT, RESTAURANTS_TEXT, COFFEE_SHOPS_TEXT,
			HAWKER_CENTRES_TEXT, COFFEE_TEXT, MALLS_TEXT, 
			ENTERTAINMENT_TEXT, TOURIST_ATTRACTIONS_TEXT, PARKS_TEXT, FITNESS_AREAS]
		buttons = [KeyboardButton(category) for category in categories]
		keyboard.add(*buttons)

		sent_message = self.bot.send_message(
			self.chat_id, CATEGORY_TEXT, reply_markup=keyboard)
		self.bot.register_next_step_handler(sent_message, self.category_handler)
	

	def category_handler(self, message: Message):
		self.category = message.text
		sent_message = self.bot.send_message(
			self.chat_id, LOCATION_TEXT, reply_markup=ReplyKeyboardRemove())
		self.bot.register_next_step_handler(sent_message, self.location_handler)
	

	def location_handler(self, message: Message):
		if not message.location:
			error_message = self.bot.reply_to(message, INVALID_LOCATION_MESSAGE)
			self.bot.register_next_step_handler(error_message, self.location_handler)
			return
		location = message.location
		self.latitude = location.latitude
		self.longitude = location.longitude
		keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
		buttons = [KeyboardButton(str(i) + KM) for i in range(1, 6)]
		keyboard.add(*buttons)
		sent_message = self.bot.send_message(
			self.chat_id, RADIUS_TEXT, reply_markup=keyboard)
		self.bot.register_next_step_handler(sent_message, self.radius_handler)
	

	def radius_handler(self, message: Message):
		accepted_values = set(str(i) + KM for i in range(1, 6))
		if message.text not in accepted_values:
			error_message = self.bot.reply_to(message, INVALID_RADIUS_MESSAGE)
			self.bot.register_next_step_handler(error_message, self.radius_handler)
			return
		self.radius = int(message.text[0]) * 1000
		sent_message = self.bot.send_message(self.chat_id, NUM_REC_MESSAGE, reply_markup=ReplyKeyboardRemove())
		self.bot.register_next_step_handler(sent_message, self.num_recommendations_handler)
		

	def num_recommendations_handler(self, message: Message):
		try:
			self.num_rec = int(message.text)
			keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
			yes_option = KeyboardButton(YES_TEXT)
			no_option = KeyboardButton(NO_TEXT)
			keyboard.add(yes_option, no_option)
			sent_message = self.bot.send_message(
				self.chat_id, ONLY_OPEN_TEXT, reply_markup=keyboard)
			self.bot.register_next_step_handler(sent_message, self.only_open_handler)
		except ValueError:
			error_message = self.bot.reply_to(message, INVALID_INT_MESSAGE)
			self.bot.register_next_step_handler(error_message, self.num_recommendations_handler)


	def only_open_handler(self, message: Message):
		accepted_values = set([YES_TEXT, NO_TEXT])
		if message.text not in accepted_values:
			error_message = self.bot.reply_to(message, INVALID_ONLY_OPEN_MESSAGE)
			self.bot.register_next_step_handler(error_message, self.only_open_handler)
			return
		self.only_open = True if message.text == YES_TEXT else False
		self.recommendation_handler()


	def recommendation_handler(self):
		params = {
			KEY: self.api_key,
			KEYWORD: self.category,
			LOCATION: f'{self.latitude},{self.longitude}',
			RADIUS: self.radius,
			OPEN_NOW: self.only_open
		}
		response = requests.request(GET_REQUEST, Recommender.NEARBY_PLACES_URL, params=params)
		results = response.json().get(RESULTS_KEY)
		results = filter(lambda x: x.get(BUSINESS_STATUS_KEY) == OPERATIONAL, results)
		results = sorted(results, key=lambda result: result.get(RATING_KEY), reverse=True)
		if not results:
			self.bot.send_message(self.chat_id, ZERO_RECOMMENDATIONS_MESSAGE)
		self.bot.send_message(self.chat_id, 
			RECOMMENDATIONS_MESSAGE.format(
				num_rec=min(self.num_rec, len(results)),
				category=self.category.lower()),
			reply_markup=ReplyKeyboardRemove())
		for i, result in enumerate(results[:self.num_rec]):
			self.send_recommendation(i, result)
		keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
		yes_option = KeyboardButton(PICK_FOR_ME_TEXT)
		no_option = KeyboardButton(PICK_MYSELF_TEXT)
		keyboard.add(yes_option, no_option)
		sent_mesasge = self.bot.send_message(
			self.chat_id, PICK_RANDOM_RECOMMENDATIONS_MESSAGE, reply_markup=keyboard)
		self.bot.register_next_step_handler(sent_mesasge, self.decision_handler, results[:self.num_rec])
			

	def send_recommendation(self, index: int, result: dict):
		price_level = result.get(PRICE_LEVEL_KEY)
		price_level_str = DOLLAR_SIGN * price_level if price_level else None
		rating = result.get(RATING_KEY)
		user_ratings_total = result.get(USER_RATINGS_TOTAL_KEY)
		is_open = result.get(OPENING_HOURS_KEY).get(OPEN_NOW_KEY)
		text = RECOMMENDATIONS_TEXT.format(
			rating=rating, user_ratings_total=user_ratings_total,
			price_level=price_level_str, open_now=is_open)
		photos = result.get(PHOTOS_KEY)
		media_photos = self.get_place_photos(photos, text)
		place_name = PLACE_NAME.format(index=index + 1, name=result.get(NAME_KEY))
		result_lat = result.get(GEOMETRY_KEY).get(LOCATION).get(LAT_KEY)
		result_lng = result.get(GEOMETRY_KEY).get(LOCATION).get(LNG_KEY)
		place_address = result.get(VICINITY_KEY)
		place_id = result.get(PLACE_ID_KEY)
		self.bot.send_venue(self.chat_id, result_lat, result_lng,
		    place_name, place_address, google_place_id=place_id)
		if media_photos:
			self.bot.send_media_group(self.chat_id, media_photos)
		if not media_photos or len(media_photos) > 1:
			self.bot.send_message(self.chat_id, text)


	def get_place_photos(self, photos: list | None, text: str):
			media_photos = []
			if not photos:
				return media_photos
			for photo in photos:
				params = {
					KEY: self.api_key,
					PHOTO_REF: photo.get(PHOTO_REF),
					MAX_HEIGHT: photo.get(HEIGHT),
					MAX_WIDTH: photo.get(WIDTH)
				}
				response = requests.request(GET_REQUEST, Recommender.PLACES_URL, params=params)
				image = Image.open(BytesIO(response.content))
				media_photo = InputMediaPhoto(image, caption=text) if len(photos) ==1 else InputMediaPhoto(image)
				media_photos.append(media_photo)
			return media_photos
	

	def decision_handler(self, message: Message, results: list):
		accepted_values = set([PICK_FOR_ME_TEXT, PICK_MYSELF_TEXT])
		if message.text not in accepted_values:
			error_message = self.bot.reply_to(message, INVALID_ONLY_OPEN_MESSAGE)
			self.bot.register_next_step_handler(error_message, self.decision_handler, results)
			return
		if message.text == PICK_MYSELF_TEXT:
			self.bot.send_message(self.chat_id,
				SIGN_OFF_TEXT, reply_markup=ReplyKeyboardRemove())
			return
		rand_index = randint(0, len(results) - 1)
		self.bot.send_message(self.chat_id,
			BOT_RECOMMENDATION_MESSAGE, reply_markup=ReplyKeyboardRemove())
		self.send_recommendation(rand_index, results[rand_index])











	
		