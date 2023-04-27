from telebot import TeleBot
from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InputMediaPhoto
from app.constants import *
import os
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from PIL import Image
from io import BytesIO
from random import randint


class Recommender:

    def __init__(self, bot: TeleBot, chat_id: str):
        self.bot = bot
        self.chat_id = chat_id
        self.category = None
        self.latitude = None
        self.longitude = None
        self.radius = None
        self.only_open = False
        self.num_rec = None
        self.max_workers = int(os.getenv(MAX_WORKERS))
        self.api_key = os.getenv(API_KEY)


    def recommend(self):
        keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        categories = [FOOD_TEXT, RESTAURANTS_TEXT, COFFEE_SHOPS_TEXT,
                      HAWKER_CENTRES_TEXT, COFFEE_TEXT, MALLS_TEXT,
                      ENTERTAINMENT_TEXT, TOURIST_ATTRACTIONS_TEXT,
                      PARKS_TEXT, FITNESS_AREAS]
        buttons = [KeyboardButton(category) for category in categories]
        keyboard.add(*buttons)
        sent_message = self.bot.send_message(self.chat_id, CATEGORY_TEXT, reply_markup=keyboard)
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
        sent_message = self.bot.send_message(self.chat_id, RADIUS_TEXT, reply_markup=keyboard)
        self.bot.register_next_step_handler(sent_message, self.radius_handler)


    def radius_handler(self, message: Message):
        accepted_values = set(str(i) + KM for i in range(1, 6))
        if message.text not in accepted_values:
            error_message = self.bot.reply_to(message, INVALID_RADIUS_MESSAGE)
            self.bot.register_next_step_handler(error_message, self.radius_handler)
            return
        self.radius = int(message.text[0]) * 1000
        keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        buttons = [KeyboardButton(str(i)) for i in range(1, 6)]
        keyboard.add(*buttons)
        sent_message = self.bot.send_message(
            self.chat_id, NUM_REC_MESSAGE, reply_markup=keyboard)
        self.bot.register_next_step_handler(sent_message, self.num_recommendations_handler)


    def num_recommendations_handler(self, message: Message):
        accepted_values = set([i for i in range(1, 6)])
        if message.text not in accepted_values:
            error_message = self.bot.reply_to(message, INVALID_INT_MESSAGE)
            self.bot.register_next_step_handler(error_message, self.num_recommendations_handler)
            return
        self.num_rec = int(message.text)
        keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        yes_option = KeyboardButton(YES_TEXT)
        no_option = KeyboardButton(NO_TEXT)
        keyboard.add(yes_option, no_option)
        sent_message = self.bot.send_message(self.chat_id, ONLY_OPEN_TEXT, reply_markup=keyboard)
        self.bot.register_next_step_handler(sent_message, self.only_open_handler)
            

    def only_open_handler(self, message: Message):
        accepted_values = set([YES_TEXT, NO_TEXT])
        if message.text not in accepted_values:
            error_message = self.bot.reply_to(message, INVALID_ONLY_OPEN_MESSAGE)
            self.bot.register_next_step_handler(error_message, self.only_open_handler)
            return
        self.only_open = True if message.text == YES_TEXT else False
        self.recommendation_handler()


    def recommendation_handler(self):
        self.bot.send_chat_action(self.chat_id, TYPING)
        params = {
            KEY: self.api_key,
            KEYWORD: self.category,
            LOCATION: f'{self.latitude},{self.longitude}',
            RADIUS: self.radius,
            OPEN_NOW: self.only_open
        }
        response = requests.request(GET_REQUEST, os.getenv(NEARBY_PLACES_URL), params=params)
        results = response.json().get(RESULTS_KEY)
        results = filter(lambda x: x.get(BUSINESS_STATUS_KEY) == OPERATIONAL, results)
        results = sorted(results, key=lambda result: result.get(RATING_KEY), reverse=True)
        if not results:
            self.bot.send_message(self.chat_id, ZERO_RECOMMENDATIONS_MESSAGE)
            return
        self.bot.send_message(self.chat_id,RECOMMENDATIONS_MESSAGE.format(
                num_rec=min(self.num_rec, len(results)),category=self.category.lower()),
            reply_markup=ReplyKeyboardRemove())
        
        recommendations = []        
        for i, result in enumerate(results[:self.num_rec]):
            recommendation = self.get_recommendation_details(i, result.get(PLACE_ID_KEY))
            self.send_recommendation(recommendation)
            recommendations.append(recommendation)
                
        if len(recommendations) == 1:
            return
        keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        yes_option = KeyboardButton(PICK_FOR_ME_TEXT)
        no_option = KeyboardButton(PICK_MYSELF_TEXT)
        keyboard.add(yes_option, no_option)
        sent_mesasge = self.bot.send_message(
            self.chat_id, PICK_RANDOM_RECOMMENDATIONS_MESSAGE, reply_markup=keyboard)
        self.bot.register_next_step_handler(sent_mesasge, 
                                            self.decision_handler, recommendations)


    def get_recommendation_details(self, index: int, place_id: str):
        self.bot.send_chat_action(self.chat_id, TYPING)
        params = {KEY: self.api_key, PLACE_ID_KEY: place_id}
        response = requests.request(GET_REQUEST, os.getenv(PLACE_DETAILS_URL), params=params)
        result = response.json().get(RESULT_KEY)
        price_level = result.get(PRICE_LEVEL_KEY)
        price_level_str = DOLLAR_SIGN * price_level if price_level else None
        rating = result.get(RATING_KEY)
        user_ratings_total = result.get(USER_RATINGS_TOTAL_KEY)
        is_open = result.get(OPENING_HOURS_KEY).get(OPEN_NOW_KEY)
        opening_hours = NEW_LINE.join(result.get(OPENING_HOURS_KEY).get(WEEKDAY_TEXT_KEY))
        contact_info = result.get(PHONE_NUMBER_KEY)
        website = result.get(WEBSITE_KEY)
        place_editorial_summary = result.get(EDITORIAL_SUMMARY_KEY)
        place_overview = place_editorial_summary.get(OVERVIEW_KEY) if place_editorial_summary else None
        options = self.get_place_options(result)
        serves = self.get_place_serves(result)
        text = RECOMMENDATIONS_TEXT.format(
                overview=place_overview, rating=rating, 
                user_ratings_total=user_ratings_total, price_level=price_level_str,
                contact_info=contact_info ,website=website, options=options, serves=serves,
                open_now=is_open, opening_hours=opening_hours)
        photos = result.get(PHOTOS_KEY)
        media_photos = self.get_media_photos(photos, text)
        return {
            INDEX_KEY: index,
            RECOMMENDATION_TEXT_KEY: text,
            MEDIA_PHOTOS_KEY: media_photos,
            NAME_KEY: result.get(NAME_KEY),
            PLACE_ID_KEY: place_id,
            FORMATTED_ADDRESS_KEY: result.get(FORMATTED_ADDRESS_KEY),
            LAT_KEY: result.get(GEOMETRY_KEY).get(LOCATION).get(LAT_KEY),
            LNG_KEY: result.get(GEOMETRY_KEY).get(LOCATION).get(LNG_KEY)
        }
    

    def send_recommendation(self, recommendation: dict):
        place_name = PLACE_NAME.format(index=recommendation.get(INDEX_KEY) + 1,
                                        name=recommendation.get(NAME_KEY))
        sent_venue = self.bot.send_venue(self.chat_id, 
            recommendation.get(LAT_KEY),
            recommendation.get(LNG_KEY), place_name, 
            recommendation.get(FORMATTED_ADDRESS_KEY),
            google_place_id=recommendation.get(PLACE_ID_KEY))
        recommendation[VENUE_MESSAGE_KEY] = sent_venue
        media_photos = recommendation.get(MEDIA_PHOTOS_KEY)
        if media_photos:
            self.bot.send_chat_action(self.chat_id, UPLOAD_PHOTO)
            self.bot.send_media_group(self.chat_id, media_photos)
        if not media_photos or len(media_photos) > 1:
            self.bot.send_chat_action(self.chat_id, TYPING)
            self.bot.send_message(self.chat_id, 
                                  recommendation.get(RECOMMENDATION_TEXT_KEY))


    def get_media_photos(self, photos: list | None, text: str):
        self.bot.send_chat_action(self.chat_id, TYPING)
        media_photos = []
        if not photos:
            return media_photos
        if len(photos) > 1:
            text = None
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = [executor.submit(self.get_media_photo, photo, text) for photo in photos]
            for future in as_completed(futures):
                media_photo = future.result()
                media_photos.append(media_photo)
        return media_photos


    def get_media_photo(self, photo: dict, text: str | None) -> InputMediaPhoto:
        params = {
            KEY: self.api_key,
            PHOTO_REF: photo.get(PHOTO_REF),
            MAX_HEIGHT: photo.get(HEIGHT),
            MAX_WIDTH: photo.get(WIDTH)
        }
        response = requests.request(GET_REQUEST, os.getenv(PLACE_PHOTO_URL), params=params)
        image = Image.open(BytesIO(response.content))
        return InputMediaPhoto(image, caption=text) if text else InputMediaPhoto(image)



    def get_place_options(self, result: dict) -> str | None:
        options = []
        if result.get(DINE_IN_KEY):
            options.append(DINE_IN)
        if result.get(TAKE_OUT_KEY):
            options.append(TAKE_OUT)
        if result.get(DELIVERY_KEY):
            options.append(DELIVERY)
        if result.get(RESERVABLE_KEY):
            options.append(RESERVABLE_KEY.capitalize())
        return f'{COMMA} '.join(options) if options else None

     
    def get_place_serves(self, result: dict) -> str | None:
        serves = []
        if result.get(SERVES_BREAKFAST_KEY):
            serves.append(BREAKFAST)
        if result.get(SERVES_BRUNCH_KEY):
            serves.append(BRUNCH)
        if result.get(SERVES_LUNCH_KEY):
            serves.append(LUNCH)
        if result.get(SERVES_DINNER_KEY):
            serves.append(DINNER)
        if result.get(SERVES_VEG_FOOD_KEY):
            serves.append(VEG_FOOD)
        if result.get(SERVES_BEER_KEY):
            serves.append(BEER)
        if result.get(SERVES_WINE_KEY):
            serves.append(WINE)
        return f'{COMMA} '.join(serves) if serves else None


    def decision_handler(self, message: Message, results: list):
        accepted_values = set([PICK_FOR_ME_TEXT, PICK_MYSELF_TEXT])
        if message.text not in accepted_values:
            error_message = self.bot.reply_to(message, INVALID_ONLY_OPEN_MESSAGE)
            self.bot.register_next_step_handler(error_message, self.decision_handler, results)
            return
        if message.text == PICK_MYSELF_TEXT:
            self.bot.send_message(self.chat_id,SIGN_OFF_TEXT,
                                  reply_markup=ReplyKeyboardRemove())
            return
        rand_index = randint(0, len(results) - 1)
        name = results[rand_index].get(NAME_KEY)
        venue_message = results[rand_index].get(VENUE_MESSAGE_KEY)
        self.bot.reply_to(venue_message, BOT_RECOMMENDATION_MESSAGE.format(name=name),
                          reply_markup=ReplyKeyboardRemove())

