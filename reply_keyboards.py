from telegram import ReplyKeyboardMarkup

township_first_consonant_keyboard = ReplyKeyboardMarkup(
    [['က', 'စ', 'တ', 'ဒ'], ['ပ', 'ဗ', 'မ', 'ရ',] ,['လ', 'သ', 'အ', 'ဥ']],
    one_time_keyboard=True, resize_keyboard=True, input_field_placeholder="First consonant of township"
)

township_keyboards_dict = {
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

category_keyboard = ReplyKeyboardMarkup(
    [
        ["လမ်းကြောင်း", "ခေတ္တရပ်စောင့်/ကားပေါ််ကခေတ္တဆင်း"], ['ထောက်လှမ်း', "Camp/ဝပ်ကျင်း", "ကင်းပုန်း"], 
        ["*စစ်ဆေးခြင်း/ဖမ်းစီးခြင်း*"],
        ["လမ်းအတားအဆီးများ"], ["Others"], ["ပစ်ခတ်/ေပါက်ကွဲသံ"], ["ဒလန်"]
    ], resize_keyboard=True, one_time_keyboard=True
)

check_point_keyboard = ReplyKeyboardMarkup(
    [["ဧည့်စာရင်း", "လူရှာခြင်း"], ["ယာဉ်စစ်", "ဖုန်းစစ်"]], resize_keyboard=True, one_time_keyboard=True
)
 
Others_keyboard = ReplyKeyboardMarkup(
    [["ခြိမ်းေခြာက်", "Drone", "CCTV"], 
    ["လူမှုပြဿနာ", "အိမ်ချိတ်ပိတ်", "လော်‌နဲ့ကြေငြာ"], 
    ["မီးကြိုးဖြတ်", "ကျူးရှင်း", "မီးလောင်"], 
    ["None of the above"]], resize_keyboard=True, one_time_keyboard=True
)

confirmaion_keyboard = ReplyKeyboardMarkup(
    [["Yes", "No"]], resize_keyboard=True, one_time_keyboard=True,
)