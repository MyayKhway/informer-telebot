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
from inline_kb import StrengthPicker, TimePicker
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

TIME, TOWN_ALPHABET, TOWNSHIP, CATEGORY, CATEGORY1, PIN_LOCATION, TEXT_LOCATION, DESCRIPTION, STRENGTH, ATTACHMENT, SOURCE = range(11)
inline_for_strength = StrengthPicker()
inline_for_time = TimePicker()
def start(update: Update, context: CallbackContext) -> int:
    """Start the conversation and asks the user about when it happened"""
    update.message.reply_text(
        "Choose the time of the event", reply_markup=inline_for_time.keyboard,
    )
    return TIME

def handle_time_callback(update: Update, context: CallbackContext) -> int:
    """Handle callback for timepicker and ask the town alpha when submitted"""
    global inline_for_time
    query = update.callback_query
    query.answer()
    if query.data == "hour_inc":
        inline_for_time.inc_hour()
    elif query.data == "hour_dec":
        inline_for_time.dec_hour()
    elif query.data == "minute_inc":
        inline_for_time.inc_minute()
    elif query.data == "minute_dec":
        inline_for_time.dec_minute()
    elif query.data == "submit":
        """Save the time and ask for category"""
        query.delete_message()
        query.bot.send_message(
            query.from_user.id,
        " Choose the first letter of the township where it happened."
        "North Dagon, South Dagon, East Dagon begins with ဒ and North and South Okkalapa begins with ဥ",
        reply_markup=township_first_consonant_keyboard,
        )
        return TOWN_ALPHABET
    query.edit_message_text(
        "Press Ok after you have chosen", reply_markup=inline_for_time.keyboard
    )
    return TIME

def choose_township(update: Update, context: CallbackContext) -> int:
    # choose the township 
    kb_dict = township_keyboards_dict
    chosen_consonant = update.message.text
    update.message.reply_text(
        "Choose the township",
        reply_markup=ReplyKeyboardMarkup(
           kb_dict.get(chosen_consonant),resize_keyboard=True, one_time_keyboard=True, input_field_placeholder="Township"), 
        )
    return TOWNSHIP 

def ask_category(update: Update, context: CallbackContext) -> int:
    """Save township and ask category"""
    update.message.reply_text(
        "Categorise the event",
        reply_markup=category_keyboard, 
        )
    return CATEGORY

def category1(update: Update, context: CallbackContext) -> int: 
    if update.message.text == "Others":
        update.message.reply_text(
            "Choose the category, choose none of the above if you cannot categorize", reply_markup=Others_keyboard
        )
        return CATEGORY1
    elif update.message.text == "*စစ်ဆေးခြင်း/ဖမ်းစီးခြင်း*":
        update.message.reply_text(
            "Choose the category,", reply_markup=check_point_keyboard,
            parse_mode='Markdown',
        )
        return CATEGORY1
    else:
        """Save the category and ask town consonant"""
        update.message.reply_text(
            """Send when the event occured, Pick a time and press OK to submit""",
            reply_markup=inline_for_time.keyboard
        )
        return PIN_LOCATION

def save_category_pin_location(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        """Pin the location"""
    )
    return PIN_LOCATION

def save_location_ask_text_location(update: Update, context: CallbackContext) -> int:
    """save pin location ask for location in text"""
    update.message.reply_text(
        """Now send the location of the event in text, you can put here landmarks nearby or the floor of the apartment building
        If you have nothing to add, press space and skip""",
    )
    return TEXT_LOCATION

def save_text_location_ask_description(update: Update, context: CallbackContext) -> int:
    """Save text location and ask for description"""
    update.message.reply_text(
        """Write the detailed description of what happened"""
    )
    return DESCRIPTION

def save_description_ask_strength(update: Update, context:CallbackContext) -> int:
    """Save description and ask the number of forces"""
    update.message.reply_text(
        """Choose the estimated number of forces you saw"""
    )
    return STRENGTH

def save_strength_ask_attachment(update: Update, context:CallbackContext) -> int:
    """Save strength and ask for attachment if any"""
    update.message.reply_text(
        """Would you like to add some attachment to this information?"""
    )
    return ATTACHMENT

def save_attachment_ask_source(update: Update, context: CallbackContext) -> int:
    """Save attachment and ask source"""
    update.message.reply_text(
        """What is the source?"""
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
            TIME : [CallbackQueryHandler(handle_time_callback)],
            TOWN_ALPHABET : [MessageHandler(Filters.text, choose_township)],
            TOWNSHIP : [MessageHandler(Filters.text, ask_category)],
            CATEGORY : [MessageHandler(Filters.text, category1)],
            CATEGORY1 : [MessageHandler(Filters.text, save_category_pin_location)],
            PIN_LOCATION : [MessageHandler(Filters.location, save_location_ask_text_location)],
            TEXT_LOCATION : [MessageHandler(Filters.text, save_text_location_ask_description)],
            DESCRIPTION : [MessageHandler(Filters.text, save_description_ask_strength)],
            STRENGTH : [MessageHandler(Filters.text,  save_strength_ask_attachment)],
            ATTACHMENT : [MessageHandler(Filters.text, save_attachment_ask_source)],
        },
        fallbacks=[CommandHandler('cancel',cancel)],
    )

    dispatcher.add_handler(conv_handler)

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
    