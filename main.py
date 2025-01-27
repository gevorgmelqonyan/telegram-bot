import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN = "7963080083:AAFn7tJeLhCXxrrTml4Kjm20mcpyduq7a1k"
CHANNEL_USERNAME = "@bluebee_am"

bot = telebot.TeleBot(API_TOKEN)
# Կոճակների ստեղծում
def create_start_keyboard():
    keyboard = InlineKeyboardMarkup()
    # Բաժանորդագրվելու կոճակը՝ ալիքի հղմամբ
    subscribe_button = InlineKeyboardButton(
        "Բաժանորդագրվել", url=f"https://t.me/{CHANNEL_USERNAME.lstrip('@')}?start=bot")
    # Բաժանորդագրության ստուգման կոճակը
    check_subscription_button = InlineKeyboardButton("Բաժանորդագրվել եմ", callback_data="check_subscription")
    keyboard.add(subscribe_button)
    keyboard.add( check_subscription_button)
    return keyboard

@bot.message_handler(commands=['start'])
def send_welcome(message):
    keyboard = create_start_keyboard()
    bot.send_message(
        message.chat.id,
        "Խաղի հղումը ստանալու համար նախ բաժանորդագրվիր մեր ալիքին",
        reply_markup=keyboard
    )

@bot.callback_query_handler(func=lambda call: call.data == "check_subscription")
def check_subscription(call):
    user_id = call.from_user.id
    try:
        # Ստուգում ենք, թե օգտատերը բաժանորդագրված է արդյոք
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        if member.status in ["member", "administrator", "creator"]:
            # Եթե բաժանորդագրված է, ուղարկում ենք շնորհակալություն և նկարը
                bot.send_message(chat_id=call.message.chat.id, text = "https://liveball.uno/match/1199389")
        else:
            # Եթե չի բաժանորդագրված
            bot.answer_callback_query(call.id, "Դուք բաժանորդագրված չեք ալիքին, բաժանորդագրվեք հղումը ստանալու համար", show_alert=True)
    except Exception as e:
        # Սխալների հետ հաղորդագրություն
        bot.answer_callback_query(call.id, "Չհաջողվեց ստուգել բաժանորդագրությունը:", show_alert=True)
        print(e)

if __name__ == "__main__":
    bot.infinity_polling(none_stop=True)
