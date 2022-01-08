import os
import logging
from dotenv.main import load_dotenv
from telegram.inline.inlinekeyboardbutton import InlineKeyboardButton
from reply_keyboards import (
    township_first_consonant_keyboard,
    township_keyboards_dict,
    category_keyboard,
    check_point_keyboard,
    Others_keyboard,
    confirmaion_keyboard,
)
from inline_kb import StrengthPicker, TimePicker
from telegram import ReplyKeyboardMarkup, Update, ReplyKeyboardRemove, replymarkup
from telegram.ext import (
    Updater,
    CommandHandler, 
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
    CallbackQueryHandler,
)
from sendtoAT import create_record

# Enable Loggin
logging.basicConfig( 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

TIME, TOWN_ALPHABET, TOWNSHIP, CATEGORY, CATEGORY1, PIN_LOCATION, TEXT_LOCATION, DESCRIPTION, VEHICLE_STRENGTH, PERSONNEL_STRENGTH, ATTACHMENT, SOURCE, CONFIRMATION = range(13)

def start(update: Update, context: CallbackContext) -> int:
    global inline_for_time
    inline_for_time = TimePicker()
    """Start the conversation and asks the user about when it happened"""
    update.message.reply_text(
        "အကြောင်းအရာဖြစ်ပျက်ချိန်ကို ရွေးချယ်ပါ။ ပြီးရင် OK နှိပ်ပါ။", reply_markup=inline_for_time.keyboard,
    )
    context.user_data['reporter_tele_id'] = str(update.message.from_user.id)
    context.user_data['reporter_name'] = update.message.from_user.name
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
        year = str(inline_for_time.current_time.year)
        month = str(inline_for_time.current_time.month)
        day = str(inline_for_time.current_time.day)
        hour_int = int(inline_for_time.hour_face.text)
        hour = str(hour_int) if hour_int >= 10 else "0" + str(hour_int) 
        minute_int = int(inline_for_time.minute_face.text)
        minute = str(minute_int) if minute_int >= 10 else "0" + str(minute_int) 
        d = "-".join([year, month, day])
        t = ":".join([hour, minute,])
        dt = ("T".join([d, t])) + ":00.000Z"
        context.user_data['time_of_event'] = dt
        query.delete_message()
        query.bot.send_message(
            query.from_user.id,
        "ဖြစ်ပျက်သွားသော မြို့နယ်၏ အစ စကားလုံးကိုရွေးချယ်ပါ။(ဥပမာ - ကမာရွတ် အတွက် 'က')",
        reply_markup=township_first_consonant_keyboard,
        )
        inline_for_time.reset()
        return TOWN_ALPHABET
    query.edit_message_text(
        "အကြောင်းအရာဖြစ်ပျက်ချိန်ကို ရွေးချယ်ပါ။ ပြီးရင် OK နှိပ်ပါ။", reply_markup=inline_for_time.keyboard
    )
    return TIME

def choose_township(update: Update, context: CallbackContext) -> int:
    # choose the township 
    kb_dict = township_keyboards_dict
    chosen_consonant = update.message.text
    update.message.reply_text(
        "မြို့နယ်ရွေးချယ်ပါ။",
        reply_markup=ReplyKeyboardMarkup(
           kb_dict.get(chosen_consonant),resize_keyboard=True, one_time_keyboard=True, input_field_placeholder="Township"), 
        )
    return TOWNSHIP 

def ask_category(update: Update, context: CallbackContext) -> int:
    """Save township and ask category"""
    context.user_data['township'] = update.message.text
    update.message.reply_text(
        "သတင်းအမျိုးအစားကို ‌ရွေးချယ်ပါ။",
        reply_markup=category_keyboard, 
        )
    return CATEGORY

def category1(update: Update, context: CallbackContext) -> int: 
    if update.message.text == "Others":
        update.message.reply_text(
            "သတင်းအမျိုးအစားကို ‌ရွေးချယ်ပါ။", reply_markup=Others_keyboard
        )
        return CATEGORY1
    elif update.message.text == "*စစ်ဆေးခြင်း/ဖမ်းစီးခြင်း*":
        update.message.reply_text(
            "သတင်းအမျိုးအစားကို ‌ရွေးချယ်ပါ။", reply_markup=check_point_keyboard,
        )
        return CATEGORY1
    else:
        """Save the category and ask location pin"""
        context.user_data['category'] = update.message.text
        update.message.reply_text(
            """ဖြစ်ပျက်သွားသောနေရာကို မြေပုံထောက်ပေးပါ။ (📎ကိုနှိပ်ပြီး Location တွင် မြေပုံထောက်ရွေးချယ် နိုင်ပါသည်။)""",
        )
        return PIN_LOCATION

def save_category_pin_location(update: Update, context: CallbackContext) -> int:
    context.user_data['category'] = update.message.text
    update.message.reply_text(
        """ဖြစ်ပျက်သွားသောနေရာကို မြေပုံထောက်ပေးပါ။ (📎ကိုနှိပ်ပြီး Location တွင် မြေပုံထောက်ရွေးချယ် နိုင်ပါသည်။)"""
    )
    return PIN_LOCATION

def save_location_ask_text_location(update: Update, context: CallbackContext) -> int:
    """save pin location ask for location in text"""
    coordinates = ",".join([str(update.message.location.latitude), str(update.message.location.longitude)])
    context.user_data['location_coordinates'] = coordinates
    update.message.reply_text(
        """ဖြစ်ပျက်သွားသောနေရာကို စာဖြင့် အသေးစိတ်ဖော်ပြပါ။ 
        ထင်ရှားသောနေရာများ၊ တိုက်အလွှာများ၊ လမ်းကြောင်း ဦးတည်ရာများ ထည့်ရေးနိုင်သည်။ 
        (ဥပမာ - YMBA အနောက်ပေါက် (သို့) မလွှကုန်းမှ တာမွေဈေးဘက်)""")
    return TEXT_LOCATION

def save_text_location_ask_description(update: Update, context: CallbackContext) -> int:
    """Save text location and ask for description"""
    location_text = update.message.text
    context.user_data['location_text'] = location_text
    update.message.reply_text(
        """အဖြစ်အပျက် အသေးစိတ်ကို ဖော်ပြပါ။"""
    )
    return DESCRIPTION

def save_description_ask_strength(update: Update, context:CallbackContext) -> int:
    """Save description and ask the number of forces"""
    global inline_for_strength
    inline_for_strength = StrengthPicker()
    desc = update.message.text
    context.user_data['description'] = desc
    if context.user_data['category'] in ["ခြိမ်းေခြာက်", "Drone", "CCTV", "လူမှုပြဿနာ", "အိမ်ချိတ်ပိတ်", "လော်‌နဲ့ကြေငြာ", "ပစ်ခတ်/ေပါက်ကွဲသံ", "ဒလန်" ]:
        update.message.reply_text(
        """အကြောင်းအရာနှင့် ပတ်သက်ပြီး အသံဖိုင် ဓါတ်ပုံ ဗီဒီယို ပေးပို့လိုပါသလား?""", reply_markup=confirmaion_keyboard,
        )
        return ATTACHMENT
    update.message.reply_text(
        """ကား အစီးရေကို ရွေးချယ်ပါ။ ပြီးရင် OK နှိပ်ပါ။""", reply_markup=inline_for_strength.vehicle_keyboard,
    )
    return VEHICLE_STRENGTH

def handle_strength_callback(update: Update, context: CallbackContext) -> int:
    global inline_for_strength
    """Save the vehicle number and ask for personnel number"""
    query = update.callback_query
    query.answer()
    if query.data == "small_vehicle_inc":
        inline_for_strength.inc_small()
    if query.data == "small_vehicle_dec":
        inline_for_strength.dec_small()
    if query.data == "large_vehicle_inc":
        inline_for_strength.inc_large()
    if query.data == "large_vehicle_dec":
        inline_for_strength.dec_large()
    if query.data == "civ_vehicle_inc":
        inline_for_strength.inc_civ()
    if query.data == "civ_vehicle_dec":
        inline_for_strength.dec_civ()
    if query.data == "motorbike_inc":
        inline_for_strength.inc_motor()
    if query.data == "motorbike_dec":
        inline_for_strength.dec_motor()
    if query.data == "other_vehicle_inc":
        inline_for_strength.inc_other()
    if query.data == "other_vehicle_dec":
        inline_for_strength.dec_other()
    elif query.data == "submit":
        """Save here"""
        context.user_data['small_vehicle'] = int(inline_for_strength.small_vehicle_number_button.text)
        context.user_data['large_vehicle'] = int(inline_for_strength.large_vehicle_number_button.text)
        context.user_data['other_vehicle']= int(inline_for_strength.other_vehicle_number_button.text)
        context.user_data['civ_vehicle'] = int(inline_for_strength.civ_vehicle_number_button.text)
        context.user_data['motorbike'] = int(inline_for_strength.motorbike_number_button.text)
        query.delete_message()
        query.bot.send_message(
            query.from_user.id,
            """ရန်သူအင်အားကို ရွေးချယ်ပါ။ ပြီးရင် OK နှိပ်ပါ။""", reply_markup=inline_for_strength.personnel_keyboard
        )
        inline_for_strength.reset_vehicle()
        return PERSONNEL_STRENGTH
    query.edit_message_text(
        """ကား အစီးရေကို ရွေးချယ်ပါ။ ပြီးရင် OK နှိပ်ပါ။""", reply_markup= inline_for_strength.vehicle_keyboard
    ) 
    return VEHICLE_STRENGTH

def handle_personnel_strength_callback(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    if query.data == "uniform_inc":
        inline_for_strength.inc_uniform()
    if query.data == "uniform_dec":
        inline_for_strength.dec_uniform()
    if query.data == "plain_inc":
        inline_for_strength.inc_plain()
    if query.data == "plain_dec":
        inline_for_strength.dec_plain()
    if query.data == "submit":
        context.user_data['uniform'] = int(inline_for_strength.uniform_number_button.text)
        context.user_data['plain'] = int(inline_for_strength.plain_number_button.text)
        query.delete_message()
        query.bot.send_message(
            query.from_user.id,
        """အကြောင်းအရာနှင့် ပတ်သက်ပြီး အသံဖိုင် ဓါတ်ပုံ ဗီဒီယို ပေးပို့လိုပါသလား?""", reply_markup=confirmaion_keyboard,
        )
        inline_for_strength.reset_personnel()
        return ATTACHMENT
    query.edit_message_text(
        """ရန်သူအင်အားကို ရွေးချယ်ပါ။ ပြီးရင် OK နှိပ်ပါ။""",
        reply_markup= inline_for_strength.personnel_keyboard,
    )
    return PERSONNEL_STRENGTH

def save_strength_confirm_attachment(update: Update, context:CallbackContext) -> int:
    """Save strength and ask for attachment if any"""
    update.message.reply_text(
        """အကြောင်းအရာနှင့် ပတ်သက်ပြီး အသံဖိုင် ဓါတ်ပုံ ဗီဒီယို ပေးပို့လိုပါသလား?""", 
        reply_markup=confirmaion_keyboard,
    )
    return ATTACHMENT

def ask_for_attachment(update: Update, context: CallbackContext) -> int:
    if update.message.text == "Yes":
        update.message.reply_text(
            """ဓါတ်ပုံ ဗီဒီယို ပေးပို့လိုပါ က📎 တွင် attachment တွဲပြီး ပေးပို့နိုင်ပါသည်။""",
        )
        return ATTACHMENT
    else:
        update.message.reply_text(
            """သတင်းရင်းမြစ်ကို ဖော်ပြပေးပါ။"""
        )
    return SOURCE
    
def save_photo_ask_source(update: Update, context: CallbackContext) -> int:
    file = update.message.photo[-1].get_file()
    filename = context.user_data["time_of_event"] + context.user_data["township"]
    context.user_data["attachment"] = [
        {
            "url" : file.file_path,
            "filename" : filename
        }
    ]
    update.message.reply_text(
        """သတင်းရင်းမြစ်ကို ဖော်ပြပေးပါ။"""
    )
    return SOURCE

def save_audio_ask_source(update: Update, context: CallbackContext) -> int:
    file = update.message.audio.get_file()
    filename = context.user_data["time_of_event"] + context.user_data["township"]
    context.user_data["attachment"] = [
        {
            "url" : file.file_path,
            "filename" : filename
        }
    ]
    update.message.reply_text(
        """သတင်းရင်းမြစ်ကို ဖော်ပြပေးပါ။"""
    )
    return SOURCE

def save_video_ask_source(update: Update, context: CallbackContext) -> int:
    file = update.message.video.get_file()
    filename = context.user_data["time_of_event"] + context.user_data["township"]
    context.user_data["attachment"] = [
        {
            "url" : file.file_path,
            "filename" : filename
        }
    ]
    update.message.reply_text(
        """သတင်းရင်းမြစ်ကို ဖော်ပြပေးပါ။"""
    )
    return SOURCE

def save_document_ask_source(update: Update, context: CallbackContext) -> int:
    file = update.message.document.get_file()
    filename = context.user_data["time_of_event"] + context.user_data["township"]
    context.user_data["attachment"] = [
        {
            "url" : file.file_path,
            "filename" : filename
        }
    ]
    update.message.reply_text(
        """သတင်းရင်းမြစ်ကို ဖော်ပြပေးပါ။"""
    )
    return SOURCE

def ask_confirmation(update: Update, context: CallbackContext) -> int:
    """Save source"""
    context.user_data['source'] = update.message.text
    confirmation_text = "{month} လပိုင်း {day} ရက်နေ့ {time} နာရီမှာ {township} မြို့အတွင်းဖြစ်ခဲ့တဲ့ {category} ကို သတင်းပေးမှာ သေချာပြီလား။ ဖြစ်စဉ်အသေးစိတ်က {description} ပါ။ သေချာရင် Yes လိုရိုက်ပြီး သတင်းမပေးလိုရင် No လိုရိုက်ပါ။"
    format_string = confirmation_text.format(
    month = inline_for_time.current_time.month,
    day = inline_for_time.current_time.day,
    time = context.user_data['time_of_event'][11:16],
    township = context.user_data['township'],
    category = context.user_data['category'],
    description = context.user_data['description'],
    )
    update.message.reply_text(
        format_string,
        reply_markup=confirmaion_keyboard,
    )
    return CONFIRMATION

def end_convo(update: Update, context: CallbackContext) -> int:
    print(context.user_data)
    update.message.reply_text(
        """သတင်းပေးပို့ပေးတဲ့အတွက် ကျေးဇူးတင်ပါတယ်။ သတင်းထပ်ပို့ရန် /infrom ကိုနှိပ်ပါ။""",
    )
    create_record(context.user_data)
    return ConversationHandler.END

def cancel(update: Update, context: CallbackContext) -> int:
    return ConversationHandler.END  
    
def main() -> None:
    load_dotenv()
    TOKEN = os.environ.get("BOTTOKEN")
    PORT = int(os.environ.get("PORT", '8443'))
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start), CommandHandler('inform', start)],
        states = {
            TIME : [CallbackQueryHandler(handle_time_callback)],
            TOWN_ALPHABET : [MessageHandler(Filters.text & ~Filters.command, choose_township)],
            TOWNSHIP : [MessageHandler(Filters.text & ~Filters.command, ask_category)],
            CATEGORY : [MessageHandler(Filters.text & ~Filters.command, category1)],
            CATEGORY1 : [MessageHandler(Filters.text & ~Filters.command, save_category_pin_location)],
            PIN_LOCATION : [MessageHandler(Filters.location & ~Filters.command, save_location_ask_text_location)],
            TEXT_LOCATION : [MessageHandler(Filters.text & ~Filters.command, save_text_location_ask_description)],
            DESCRIPTION : [MessageHandler(Filters.text & ~Filters.command, save_description_ask_strength)],
            VEHICLE_STRENGTH : [
                MessageHandler(Filters.text & ~Filters.command,  save_strength_confirm_attachment),
                CallbackQueryHandler(handle_strength_callback),
                ],
            PERSONNEL_STRENGTH : [
                CallbackQueryHandler(handle_personnel_strength_callback),
            ],
            ATTACHMENT : [
                MessageHandler(Filters.text & ~Filters.command, ask_for_attachment),
                MessageHandler(Filters.photo, save_photo_ask_source),
                MessageHandler(Filters.video, save_video_ask_source),
                MessageHandler(Filters.document, save_document_ask_source),
                ],
            SOURCE : [MessageHandler(Filters.text & ~Filters.command, ask_confirmation)],
            CONFIRMATION: [MessageHandler(Filters.text & ~Filters.command, end_convo)],
        },
        fallbacks=[CommandHandler('cancel',cancel)],
        conversation_timeout=300,
        allow_reentry=True,
    )

    dispatcher.add_handler(conv_handler)

    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path=TOKEN,
                          webhook_url='https://informer-telebot.herokuapp.com/' + TOKEN)

if __name__ == '__main__':
    main()