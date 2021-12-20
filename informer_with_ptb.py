import os
import logging
from typing import Dict
from dotenv.main import load_dotenv
from telegram.inline.inlinekeyboardbutton import InlineKeyboardButton
from reply_keyboards import (
    township_first_consonant_keyboard,
    township_keyboards_dict,
    category_keyboard,
    check_point_keyboard,
    Others_keyboard,
)
import inline_kb
from telegram import ReplyKeyboardMarkup, Update, ReplyKeyboardRemove
from telegram.ext import (
    Updater,
    CommandHandler, 
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
    CallbackQueryHandler,
)

# Enable Loggin
logging.basicConfig( 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

TOWN_ALPHABET, TOWNSHIP, LOCATION, TIME, CATEGORY, DESCRIPTION, SOURCE, CONFIRMATION = range(8)
inline_for_time = inline_kb.TimePicker()

def start(update: Update, context: CallbackContext) -> int:
    """Start the conversation and asks the user the start letter of township"""
    update.message.reply_text(
        "You can start informing."
        " Choose the first letter of the township where it happened."
        "North Dagon, South Dagon, East Dagon begins with ဒ and North and South Okkalapa begins with ဥ",
        reply_markup= township_first_consonant_keyboard
        )      
    return TOWN_ALPHABET

def town_alpha(update: Update, context: CallbackContext) -> int:
    # choose the township 
    kb_dict = township_keyboards_dict
    chosen_consonant = update.message.text
    update.message.reply_text(
        "Choose the township",
        reply_markup=ReplyKeyboardMarkup(
           kb_dict.get(chosen_consonant),resize_keyboard=True, one_time_keyboard=True, input_field_placeholder="Township"), 
        )
    return TOWNSHIP 

def ask_location(update: Update, context: CallbackContext) -> int:
    """Save the Township and ask for location"""
    update.message.reply_text(
        "Send the location of the event, you can pin the location by pressing attachments icon and choose location"
    )
    return LOCATION

def ask_time(update: Update, context: CallbackContext) -> int:
    """Save the location and ask for time"""
    update.message.reply_text(
        "Send when the event occured", reply_markup=inline_for_time.keyboard,
    )
    return LOCATION

def change_time(update: Update, context: CallbackContext) -> int:
    global inline_for_time
    query = update.callback_query
    query.answer()
    if query.data == "hour_inc":
        inline_for_time.hour_face.text = str(int(inline_for_time.hour_face.text) + 1)
    elif query.data == "hour_dec":
        inline_for_time.hour_face.text = str(int(inline_for_time.hour_face.text) - 1)
    elif query.data == "minute_inc":
        inline_for_time.minute_face.text = str(int(inline_for_time.minute_face.text) + 1)
    elif query.data == "minute_dec":
        inline_for_time.minute_face.text = str(int(inline_for_time.minute_face.text) - 1)
    elif query.data == "submit":
        """Save the time and ask for category"""
        query.delete_message()
        query.bot.send_message(
            query.from_user.id,
            "Time is saved, now categorise the event",
            category_keyboard, 
        )
        return CATEGORY
    query.edit_message_text(
        "Press Ok after you have chosen", reply_markup=inline_for_time.keyboard
    )
    return LOCATION


def ask_category(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        "Categorise the event",
        reply_markup=category_keyboard, 
        )
    return CATEGORY

def ask_description(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        "Type the details of what you saw"
    )
    return DESCRIPTION

def ask_source(update: Update, conetxt: CallbackContext) -> int:
    update.message.reply_text(
        "What is your source?"
    )
    return SOURCE

def ask_confirmation(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        "Are you sure you want to report that?",
        reply_markup=ReplyKeyboardMarkup(
            [["Yes"], ["No"]], resize_keyboard=True, one_time_keyboard=True
        ),
    )
    return CONFIRMATION

def cancel(update: Update, context: CallbackContext) -> int:
    return ConversationHandler.END  
    
def main() -> None:
    load_dotenv()
    TOKEN = os.getenv("TOKEN")
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states = {
            TOWN_ALPHABET : [MessageHandler(Filters.text, town_alpha)],
            TOWNSHIP : [MessageHandler(Filters.text, ask_location)],
            LOCATION : [
                MessageHandler(Filters.location, ask_time),
                CallbackQueryHandler(change_time),
            ],
            TIME : [MessageHandler(Filters.text, ask_category)],
            CATEGORY : [MessageHandler(Filters.text, ask_description)],
            DESCRIPTION : [MessageHandler(Filters.text, ask_source)],
            SOURCE: [MessageHandler(Filters.text, ask_confirmation)]
        },
        fallbacks=[CommandHandler('cancel',cancel)],
    )

    dispatcher.add_handler(conv_handler)

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
    