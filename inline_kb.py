from typing import Text
from telegram.ext import InlineQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime

class TimePicker:
    hour_text_button = InlineKeyboardButton("နာရီ", callback_data="display")
    minute_text_button = InlineKeyboardButton("မိနစ်", callback_data="display")
    hour_inc_button = InlineKeyboardButton("⬆", callback_data="hour_inc")
    minute_inc_button = InlineKeyboardButton("⬆", callback_data="minute_inc")
    hour_dec_button = InlineKeyboardButton("⬇", callback_data="hour_dec")
    minute_dec_button = InlineKeyboardButton("⬇", callback_data="minute_dec")
    ok_button = InlineKeyboardButton("OK", callback_data="submit")
    
    def __init__(self):
        self.current_time = datetime.now()
        self.hour_face = InlineKeyboardButton(str(self.current_time.hour), callback_data="hour")
        self.minute_face = InlineKeyboardButton(str(self.current_time.minute), callback_data="minute")
        self.keyboard = InlineKeyboardMarkup(
            [
                [self.hour_text_button, self.minute_text_button],
                [self.hour_inc_button, self.minute_inc_button],
                [self.hour_face, self.minute_face],
                [self.hour_dec_button, self.minute_dec_button],
                [self.ok_button]
            ]
        )

    def inc_hour(self):
        self.hour_face.text = (int(self.hour_face.text) + 1) % 24
    
    def dec_hour(self):
        self.hour_face.text = (int(self.hour_face.text) - 1) % 24

    def inc_minute(self):
        self.minute_face.text = (int(self.minute_face.text) + 1) % 60
    
    def dec_minute(self):
        self.minute_face.text = (int(self.minute_face.text) - 1) % 60

    def reset(self):
        self.hour_face.text = str(self.current_time.hour)
        self.minute_face.text = str(self.current_time.minute)

class StrengthPicker:
    small_vehicle_text_button = InlineKeyboardButton("စစ်/ရဲကားသေး", callback_data="text")
    small_vehicle_number_button = InlineKeyboardButton("0", callback_data="display")
    small_vehicle_inc_button = InlineKeyboardButton("⬆", callback_data="small_vehicle_inc")
    small_vehicle_dec_button = InlineKeyboardButton("⬇", callback_data="small_vehicle_dec")
    large_vehicle_text_button = InlineKeyboardButton("စစ်/ရဲကားကြီး", callback_data="text")
    large_vehicle_number_button = InlineKeyboardButton("0", callback_data="display")
    large_vehicle_inc_button = InlineKeyboardButton("⬆", callback_data="large_vehicle_inc")
    large_vehicle_dec_button = InlineKeyboardButton("⬇", callback_data="large_vehicle_dec")
    civ_vehicle_text_button = InlineKeyboardButton("အိမ်စီးကား", callback_data="text")
    civ_vehicle_number_button = InlineKeyboardButton("0", callback_data="display")
    civ_vehicle_inc_button = InlineKeyboardButton("⬆", callback_data="civ_vehicle_inc")
    civ_vehicle_dec_button = InlineKeyboardButton("⬇", callback_data="civ_vehicle_dec")
    motorbike_text_button = InlineKeyboardButton("ဆိုင်ကယ်", callback_data="text")
    motorbike_number_button = InlineKeyboardButton("0", callback_data="display")
    motorbike_inc_button = InlineKeyboardButton("⬆", callback_data="motorbike_inc")
    motorbike_dec_button = InlineKeyboardButton("⬇", callback_data="motorbike_dec")
    other_vehicle_text_button = InlineKeyboardButton("တခြားကား", callback_data="text")
    other_vehicle_number_button = InlineKeyboardButton("0", callback_data="display")
    other_vehicle_inc_button = InlineKeyboardButton("⬆", callback_data="other_vehicle_inc")
    other_vehicle_dec_button = InlineKeyboardButton("⬇", callback_data="other_vehicle_dec")
    uniform_text_button = InlineKeyboardButton("uniform", callback_data="text")
    uniform_number_button = InlineKeyboardButton("0", callback_data="display")
    uniform_inc_button = InlineKeyboardButton("⬆", callback_data="uniform_inc")
    uniform_dec_button = InlineKeyboardButton("⬇", callback_data="uniform_dec")
    plain_text_button = InlineKeyboardButton("အရပ်ဝတ်", callback_data="text")
    plain_number_button = InlineKeyboardButton("0", callback_data="display")
    plain_inc_button = InlineKeyboardButton("⬆", callback_data="plain_inc")
    plain_dec_button = InlineKeyboardButton("⬇", callback_data="plain_dec")
    ok_button = InlineKeyboardButton("OK", callback_data="submit")

    def __init__(self) -> None:
        self.vehicle_keyboard = InlineKeyboardMarkup(
            [
                [self.small_vehicle_text_button, self.large_vehicle_text_button], 
                [self.small_vehicle_inc_button, self.large_vehicle_inc_button], 
                [self.small_vehicle_number_button, self.large_vehicle_number_button], 
                [self.small_vehicle_dec_button, self.large_vehicle_dec_button], 
                [self.civ_vehicle_text_button, self.motorbike_text_button, self.other_vehicle_text_button],
                [self.civ_vehicle_inc_button, self.motorbike_inc_button, self.other_vehicle_inc_button],
                [self.civ_vehicle_number_button, self.motorbike_number_button, self.other_vehicle_number_button],
                [self.civ_vehicle_dec_button, self.motorbike_dec_button, self.other_vehicle_dec_button],
                [self.ok_button]
            ]
        )
        self.personnel_keyboard = InlineKeyboardMarkup(
            [
                [self.uniform_text_button, self.plain_text_button],
                [self.uniform_inc_button, self.plain_inc_button],
                [self.uniform_number_button, self.plain_number_button],
                [self.uniform_dec_button, self.plain_dec_button],
                [self.ok_button]
            ]
        )
    
    def inc_small(self):
        self.small_vehicle_number_button.text = (int(self.small_vehicle_number_button.text)) + 1

    def inc_large(self):
        self.large_vehicle_number_button.text = (int(self.large_vehicle_number_button.text)) + 1

    def inc_civ(self):
        self.civ_vehicle_number_button.text = (int(self.civ_vehicle_number_button.text)) + 1

    def inc_motor(self):
        self.motor_vehicle_number_button.text = (int(self.motor_vehicle_number_button.text)) + 1

    def inc_other(self):
        self.other_vehicle_number_button.text = (int(self.other_vehicle_number_button.text)) + 1

    def dec_small(self):
        if self.small_vehicle_number_button.text != '0':
            self.small_vehicle_number_button.text = (int(self.small_vehicle_number_button.text)) - 1

    def dec_large(self):
        if self.large_vehicle_number_button.text != '0':
            self.large_vehicle_number_button.text = (int(self.large_vehicle_number_button.text)) - 1

    def dec_civ(self):
        if self.civ_vehicle_number_button.text != '0':
            self.civ_vehicle_number_button.text = (int(self.civ_vehicle_number_button.text)) - 1

    def dec_motor(self):
        if self.motorbike_number_button.text != '0':
            self.motorbike_number_button.text = (int(self.motorbike_number_button.text)) - 1

    def dec_other(self):
        if self.other_vehicle_number_button.text != '0':
            self.other_vehicle_number_button.text = (int(self.other_vehicle_number_button.text)) - 1

    def inc_uniform(self):
        if self.uniform_number_button.text != '0':
            self.uniform_number_button.text = (int(self.uniform_number_button.text)) + 1

    def dec_uniform(self):
        if self.uniform_number_button.text != '0':
            self.uniform_number_button.text = (int(self.uniform_number_button.text)) - 1

    def inc_plain(self):
        if self.plain_number_button.text != '0':
            self.plain_number_button.text = (int(self.plain_number_button.text)) + 1

    def dec_uniform(self):
        if self.plain_number_button.text != '0':
            self.plain_number_button.text = (int(self.plain_number_button.text)) - 1