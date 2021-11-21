import telebot
import os 
import requests 
from dotenv import load_dotenv
from telebot import types

load_dotenv()
bot_token = os.getenv("TOKEN")
bot = telebot.TeleBot(bot_token)

event_dict = {}


class Event:
    def __init__(self, township):
        self.township = township
        self.time = None
        self.description = None
        self.event_type = None

# define the markup keyboards
# for townships
location_keyboard = types.ReplyKeyboardMarkup(row_width=4, one_time_keyboard=True)
Hlaing_btn = types.KeyboardButton("လှိုင်")
Insein_btn = types.KeyboardButton("အင်းစိန်")
Kyimyindine_btn = types.KeyboardButton("Kyimyindine")
Sanchaung_btn = types.KeyboardButton("စမ်းေချာင်း")
Okkalapa_btn = types.KeyboardButton("Okkalapa")
Kyautdata_btn = types.KeyboardButton("Kyautdata")
location_keyboard.add(Hlaing_btn, Insein_btn, Kyimyindine_btn, Sanchaung_btn, Okkalapa_btn, Kyautdata_btn)

# for Event Types
Event_type_markup = types.ReplyKeyboardMarkup(row_width=3, one_time_keyboard=True)
watch_dogs_btn = types.KeyboardButton("ဝပ်ကျဉ်း")
patrol_btn = types.KeyboardButton("လှည့်ကင်း")
raid_btn = types.KeyboardButton("ဝင်စီးနင်း")
mobilize_btn = types.KeyboardButton("တပ် ေရွှ့")
barrier_btn = types.KeyboardButton("အတားအစီး နဲ့လမ်းပိတ်")
check_point_btn = types.KeyboardButton("စစ် ေဆးေရး")
Event_type_markup.add(watch_dogs_btn, patrol_btn, raid_btn, mobilize_btn, barrier_btn, check_point_btn, check_point_btn)

# for confirmation 
confirmation_markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
yes_btn = types.KeyboardButton("Yes, submit it")
no_btn = types.KeyboardButton("No")
confirmation_markup.add(yes_btn, no_btn)

# Handle '/start'
@bot.message_handler(commands='start')
def start_asking(message):
    msg = bot.send_message(message.chat.id, """\
        You can start informing by typing /inform in the chat
""")

@bot.message_handler(commands=["inform"])
def start_asking(message):
    msg = bot.send_message(message.chat.id, "Where did you see the event?", reply_markup=location_keyboard) 
    bot.register_next_step_handler(msg, save_township)    

def save_township(message):
    township = message.text
    event = Event(township)
    event_dict[message.chat.id] = event
    msg = bot.send_message(message.chat.id, "Please type the time you saw the event, for example. 12:30 am or 13:45")
    bot.register_next_step_handler(msg, save_time)


def save_time(message):
    try:
        chat_id = message.chat.id
        time = message.text
        if ":" not in time:
            msg = bot.reply_to(message, 'Invalid format, Please type the time you saw the event, for example. 12:30 am or 13:45')
            bot.register_next_step_handler(msg, save_time)
            return
        event = event_dict[chat_id]
        event.time = time
        msg = bot.send_message(message.chat.id, 'Choose the event type', reply_markup=Event_type_markup)
        bot.register_next_step_handler(msg, save_event_type)
    except Exception as e:
        bot.reply_to(message, 'oooops')
        print(e)

def save_event_type(message):
    chat_id = message.chat.id
    event_type = message.text
    event = event_dict[chat_id]
    event.event_type = event_type
    msg = bot.send_message(message.chat.id, "Write the description in detail. For example, - 55ရပ်ကွက်ရုံးအနီးကဖြတ်သန်းသွားတဲ့ဆိုင်ကယ်ကို ခေါ်စစ်တာ ဆိုင်ကယ်သမားမောင်းထွက်သွားလို  လိုက်ဖမ်းနေတယ်လိုလဲသိရပါတယ်")
    bot.register_next_step_handler(msg, save_description)

def save_description(message):
    chat_id = message.chat.id
    event = event_dict[chat_id]
    event.description = message.text
    msg = bot.send_message(message.chat.id, """\
    Is this the information you want to provide?
    Time:""" + event.time + """Township:""" + event.township + """Type:""" + event.event_type + """Description:"""
    + event.description, reply_markup=confirmation_markup)


# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()

bot.infinity_polling()