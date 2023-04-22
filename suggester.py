from telebot import TeleBot
from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InputMediaPhoto
from constants import *
import os
import requests
from PIL import Image
from io import BytesIO

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
		self.is_open = None
		self.api_key = os.getenv(API_KEY_VAR_NAME)
	
	def recommend(self):
		keyboard = ReplyKeyboardMarkup(row_width=2)
		food_option = KeyboardButton(FOOD_TEXT)
		places_option = KeyboardButton(PLACES_TEXT)
		keyboard.add(food_option, places_option)

		sent_message = self.bot.send_message(
			self.chat_id, CATEGORY_TEXT, reply_markup=keyboard)
		self.bot.register_next_step_handler(sent_message, self.category_handler)
	
	def category_handler(self, message: Message):
		accepted_values = set([FOOD_TEXT, PLACES_TEXT])
		if message.text not in accepted_values:
			error_message = self.bot.reply_to(message, INVALID_CATEGORY_MESSAGE)
			self.bot.register_next_step_handler(error_message, self.category_handler)
			return
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
		keyboard = ReplyKeyboardMarkup(row_width=2)
		for i in range(1, 6):
			option = KeyboardButton(str(i) + KM)
			keyboard.add(option)
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
		keyboard = ReplyKeyboardMarkup(row_width=2)
		yes_option = KeyboardButton(YES_TEXT)
		no_option = KeyboardButton(NO_TEXT)
		keyboard.add(yes_option, no_option)
		sent_message = self.bot.send_message(
			self.chat_id, IS_OPEN_TEXT, reply_markup=keyboard)
		self.bot.register_next_step_handler(sent_message, self.is_open_handler)
	
	def is_open_handler(self, message: Message):
		accepted_values = set([YES_TEXT, NO_TEXT])
		if message.text not in accepted_values:
			error_message = self.bot.reply_to(message, INVALID_IS_OPEN_MESSAGE)
			self.bot.register_next_step_handler(error_message, self.is_open_handler)
			return
		self.is_open = True if message.text == YES_TEXT else False
		self.get_recommendations()


	def get_recommendations(self):
		params = {
			KEY: self.api_key,
			KEYWORD: self.category,
			LOCATION: f'{self.latitude},{self.longitude}',
			RADIUS: self.radius,
			OPEN_NOW: self.is_open
		}
		response = requests.request(GET_REQUEST, Recommender.NEARBY_PLACES_URL, params=params)
		results = response.json().get(RESULTS_KEY)
		results = filter(lambda x: x.get(BUSINESS_STATUS_KEY) == OPERATIONAL, results)
		results = sorted(results, key=lambda result: result.get(RATING_KEY), reverse=True)
		self.bot.send_message(self.chat_id, RECOMMENDATIONS_MESSAGE, reply_markup=ReplyKeyboardRemove())
		for i, result in enumerate(results[:3]):
			text = (f'{RATING_TEXT} {result.get(RATING_KEY)}\n'
	   				f'{USER_RATINGS_TOTAL_TEXT} {result.get(USER_RATINGS_TOTAL_KEY)}\n'
					f'{PRICE_LEVEL_TEXT} {result.get(PRICE_LEVEL_KEY)}\n'
					f'{OPEN_NOW_TEXT} {result.get(OPENING_HOURS_KEY).get(OPEN_NOW_KEY)}')
			photos = result.get(PHOTOS_KEY)
			media_photos = self.get_place_photos(photos, text)
			place_name = f'{i + 1}. {result.get(NAME_KEY)}'
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









	
		