import time

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN = "8016439844:AAGrDy-2KjhWYQPAzgDUAUEz13ujvAKWPoU"
CHANNEL_USERNAME = "@WalkersMadrid"

link = {"link" : "https://liveball.uno/match/1299124"}

bot = telebot.TeleBot(API_TOKEN)
# Կոճակների ստեղծում
def create_start_keyboard():
    keyboard = InlineKeyboardMarkup()
    # Բաժանորդագրվելու կոճակը՝ ալիքի հղմամբ
    subscribe_button = InlineKeyboardButton(
        "Բաժանորդագրվել", url=f"https://t.me/{CHANNEL_USERNAME.lstrip('@')}?start=bot")
    # Բաժանորդագրության ստուգման կոճակը
    check_subscription_button = InlineKeyboardButton("Ստանալ հղումը", callback_data="check_subscription")
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

@bot.message_handler(func=lambda message: message.text.lower().startswith("link-"))
def reset_game_link(message):
    link["link"] = message.text.split("-")[1]


@bot.callback_query_handler(func=lambda call: call.data == "check_subscription")
def check_subscription(call):
    user_id = call.from_user.id
    try:
        # Ստուգում ենք, թե օգտատերը բաժանորդագրված է արդյոք
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        if member.status in ["member", "administrator", "creator"]:
            # Եթե բաժանորդագրված է, ուղարկում ենք շնորհակալություն և նկարը
            msg = bot.send_message(chat_id=call.message.chat.id, text = link["link"])
            time.sleep(60)
            bot.delete_message(message_id=msg.message_id, chat_id=call.message.chat.id)
        else:
            # Եթե չի բաժանորդագրված
            bot.answer_callback_query(call.id, "Դուք բաժանորդագրված չեք ալիքին, բաժանորդագրվեք հղումը ստանալու համար", show_alert=True)
    except Exception as e:
        # Սխալների հետ հաղորդագրություն
        bot.answer_callback_query(call.id, "Չհաջողվեց ստուգել բաժանորդագրությունը:", show_alert=True)
        print(e)

if __name__ == "__main__":
    bot.infinity_polling(none_stop=True)
