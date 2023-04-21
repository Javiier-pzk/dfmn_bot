from telebot import TeleBot
from telebot.types import Message
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from constants import *
import os
import requests

class Recommender:
	
	GOOGLE_MAPS_API_URL = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'

	def __init__(self, bot:TeleBot, chat_id: str):
		self.bot = bot
		self.chat_id = chat_id
		self.category = None
		self.latitude = None
		self.longitude = None
		self.radius = None
		self.is_open = None
	
	def recommend(self):
		keyboard = ReplyKeyboardMarkup(row_width=2)
		food_option = KeyboardButton(FOOD_TEXT)
		places_option = KeyboardButton(PLACES_TEXT)
		keyboard.add(food_option, places_option)

		sent_message = self.bot.send_message(
			self.chat_id, CATEGORY_TEXT, reply_markup=keyboard)
		self.bot.register_next_step_handler(sent_message, self.category_handler)
	
	def category_handler(self, message: Message):
		self.category = message.text
		sent_message = self.bot.send_message(
			self.chat_id, LOCATION_TEXT, reply_markup=ReplyKeyboardRemove())
		self.bot.register_next_step_handler(sent_message, self.location_handler)
	
	def location_handler(self, message: Message):
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
		self.radius = int(message.text[0]) * 1000
		keyboard = ReplyKeyboardMarkup(row_width=2)
		yes_option = KeyboardButton(YES_TEXT)
		no_option = KeyboardButton(NO_TEXT)
		keyboard.add(yes_option, no_option)
		sent_message = self.bot.send_message(
			self.chat_id, IS_OPEN_TEXT, reply_markup=keyboard)
		self.bot.register_next_step_handler(sent_message, self.is_open_handler)
	
	def is_open_handler(self, message: Message):
		self.is_open = True if message.text == YES_TEXT else False
		self.send_nearby_places_request()
		sent_message = self.bot.send_message(
			self.chat_id, "ok", reply_markup=ReplyKeyboardRemove())


	def send_nearby_places_request(self):
		api_key = os.getenv(API_KEY_VAR_NAME)
		params = {
			KEY: api_key,
			KEYWORD: self.category,
			LOCATION: f'{self.latitude},{self.longitude}',
			RADIUS: self.radius,
			OPEN_NOW: self.is_open
		}
		response = requests.request(GET_REQUEST, Recommender.GOOGLE_MAPS_API_URL, params=params)
		print(response.text)
		print(len(response.text))






	
		