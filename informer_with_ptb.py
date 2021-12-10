import os
import logging
from typing import Dict
from dotenv.main import load_dotenv


from telegram import ReplyKeyboardMarkup, Update, ReplyKeyboardRemove
from telegram.ext import (
    Updater,
    CommandHandler, 
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

# Enable Loggin
logging.basicConfig( 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

TOWN_ALPHABET, TOWNSHIP, LOCATION, TIME, TYPE, DESCRIPTION, SOURCE = range(7)

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
        "က" : [["ကျောက်တံတား", "ကြည့်မြင်တိုင်", "ကမာရွတ်"]],
        "စ" : [["စမ်းချောင်း"]],
        "တ" : [["တာမွေ"]],
        "ဒ" : [["ဒေါပုံ", "အရှေ့ ဒဂုံ", "တောင် ဒဂုံ", "မြောက် ဒဂုံ", "ဒဂုံဆိပ်ကမ်း"]],
        "ပ" : [["ပုဇွန်တောင်", "ပန်းပဲတန်း"]],
        "ဗ" : [["ဗိုလ်တစ်ထောင်", "ဗဟန်း"]],
        "မ" : [["မင်္ဂလာဒုံ", "မင်္ဂလာတောင်ညွန့်", "မရမ်းကုန်း"]],
        "ရ" : [["ရွှေပြည်သာ", "ရန်ကင်း"]],
        "လ" : [["လမ်းမတော်", "လသာ", "လှိုင်သာယာ", "လှိုင်"]],
        "သ" : [["သင်္ယန်းကျွန်း", "သာကေတ"]],
        "အ" : [["အင်းစိန်", "အလုံ"]],
        "ဥ" : [["မြောက်ဥက္ကလာပ", "တောင်ဥက္ကလာပ"]]
    }

    update.message.reply_text(
        "Choose the township",
        reply_markup=ReplyKeyboardMarkup(
           reply_keyboard_dict.get(chosen_consonant), resize_keyboard=True, one_time_keyboard=True, input_field_placeholder="Township"), 
        )
    return TOWNSHIP 

def ask_location(update: Update, context: CallbackContext) -> int:
    """Save the Township and ask for location"""
    update.message.reply_text(
        "Send the location of the event, you can pin the location by pressing attachments icon and choose location"
    )

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
            TOWNSHIP : [MessageHandler(Filters.text, ask_location)]
        },
        fallbacks=[CommandHandler('cancel',cancel)],
    )

    dispatcher.add_handler(conv_handler)


    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
    
    