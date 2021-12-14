import os
import logging
from typing import Dict
from dotenv.main import load_dotenv
from telegram.inline.inlinekeyboardbutton import InlineKeyboardButton
import timepicker


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

TOWN_ALPHABET, TOWNSHIP, LOCATION, TIME, TYPE, DESCRIPTION, SOURCE, CONFIRMATION = range(8)
inline_for_time = timepicker.Timepicker()

def start(update: Update, context: CallbackContext) -> int:
    """Start the conversation and asks the user the start letter of township"""
    reply_keyboard = [['က', 'စ', 'တ', 'ဒ'], ['ပ', 'ဗ', 'မ', 'ရ',] ,['လ', 'သ', 'အ', 'ဥ']]
    update.message.reply_text(
        "You can start informing."
        " Choose the first letter of the township where it happened."
        "North Dagon, South Dagon, East Dagon begins with ဒ and North and South Okkalapa begins with ဥ",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, row_width=4, one_time_keyboard=True, input_field_placeholder="The first letter of the township"
            ),
        )
    return TOWN_ALPHABET

def town_alpha(update: Update, context: CallbackContext) -> int:
    # choose the township 
    chosen_consonant = update.message.text
    reply_keyboard_dict = {
        "က" : [["ကျောက်တံတား"], ["ကြည့်မြင်တိုင်"], ["ကမာရွတ်"]],
        "စ" : [["စမ်းချောင်း"]],
        "တ" : [["တာမွေ"]],
        "ဒ" : [["ဒေါပုံ", "အရှေ့ ဒဂုံ"], ["တောင် ဒဂုံ", "မြောက် ဒဂုံ"], ["ဒဂုံဆိပ်ကမ်း"]],
        "ပ" : [["ပုဇွန်တောင်", "ပန်းပဲတန်း"]],
        "ဗ" : [["ဗိုလ်တစ်ထောင်", "ဗဟန်း"]],
        "မ" : [["မင်္ဂလာဒုံ"], ["မင်္ဂလာတောင်ညွန့်"], ["မရမ်းကုန်း"]],
        "ရ" : [["ရွှေပြည်သာ", "ရန်ကင်း"]],
        "လ" : [["လမ်းမတော်", "လသာ"], ["လှိုင်သာယာ", "လှိုင်"]],
        "သ" : [["သင်္ယန်းကျွန်း", "သာကေတ"]],
        "အ" : [["အင်းစိန်", "အလုံ"]],
        "ဥ" : [["မြောက်ဥက္ကလာပ", "တောင်ဥက္ကလာပ"]]
    }

    update.message.reply_text(
        "Choose the township",
        reply_markup=ReplyKeyboardMarkup(
           reply_keyboard_dict.get(chosen_consonant),resize_keyboard=True, one_time_keyboard=True, input_field_placeholder="Township"), 
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
    reply_keyboard = [
        ["သပိတ်","အပစ်အခတ်"],
        ["လမ်းပိတ်", "ပေါက်ကွဲ"],
        ["တားစစ်", "ရန်သူလှုပ်ရှားမှု"],
        ["CCTV", "ကင်းပုန်း"],
        ["ဒလန်", "ဧည့်စာရင်း"],
    ]
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
        """Save the time and ask for type"""
        query.delete_message()
        query.bot.send_message(
            query.from_user.id,
            "Time is saved, now categorise the event",reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, resize_keyboard=True, one_time_keyboard=True, input_field_placeholder="Category"
            ),
        )
        return TYPE
    query.edit_message_text(
        "Press Ok after you have chosen", reply_markup=inline_for_time.keyboard
    )
    return LOCATION


def ask_type(update: Update, context: CallbackContext) -> int:
    reply_keyboard = [
        ["သပိတ်","အပစ်အခတ်"],
        ["လမ်းပိတ်", "ပေါက်ကွဲ"],
        ["တားစစ်", "ရန်သူလှုပ်ရှားမှု"],
        ["CCTV", "ကင်းပုန်း"],
        ["ဒလန်", "ဧည့်စာရင်း"],
    ]
    update.message.reply_text(
        "Categorise the event",reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, resize_keyboard=True, one_time_keyboard=True, input_field_placeholder="Category"
        )
    )
    return TYPE

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
            TIME : [MessageHandler(Filters.text, ask_type)],
            TYPE : [MessageHandler(Filters.text, ask_description)],
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
    