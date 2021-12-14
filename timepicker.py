from telegram.ext import InlineQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime

class Timepicker:
    hour_inc_button = InlineKeyboardButton("⬆", callback_data="hour_inc")
    minute_inc_button = InlineKeyboardButton("⬆", callback_data="minute_inc")
    hour_dec_button = InlineKeyboardButton("⬇", callback_data="hour_dec")
    minute_dec_button = InlineKeyboardButton("⬇", callback_data="minute_dec")
    ok_button = InlineKeyboardButton("OK", callback_data="submit")
    hour = datetime.now().hour
    minute = datetime.now().minute
    hour_face = InlineKeyboardButton(str(hour), callback_data="hour")
    minute_face = InlineKeyboardButton(str(minute), callback_data="minute")
    
    def __init__(self):
        self.keyboard = InlineKeyboardMarkup(
            [
                [self.hour_inc_button, self.minute_inc_button],
                [self.hour_face, self.minute_face],
                [self.hour_dec_button, self.minute_dec_button],
                [self.ok_button]
            ]
        )