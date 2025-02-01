import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN = "8016439844:AAGrDy-2KjhWYQPAzgDUAUEz13ujvAKWPoU"
CHANNEL_USERNAME = "@WalkersMadrid"

link = {"link": "https://liveball.uno/match/1299124"}

bot = telebot.TeleBot(API_TOKEN)


def create_start_keyboard():
    keyboard = InlineKeyboardMarkup()
    subscribe_button = InlineKeyboardButton(
        "Բաժանորդագրվել", url=f"https://t.me/{CHANNEL_USERNAME.lstrip('@')}?start=bot"
    )
    check_subscription_button = InlineKeyboardButton(
        "Ստանալ հղումը", callback_data="check_subscription"
    )
    keyboard.add(subscribe_button)
    keyboard.add(check_subscription_button)
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
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        if member.status in ["member", "administrator", "creator"]:
            msg = bot.send_message(chat_id=call.message.chat.id, text=link["link"])

        else:
            bot.answer_callback_query(call.id, "Դուք բաժանորդագրված չեք ալիքին, բաժանորդագրվեք հղումը ստանալու համար",
                                      show_alert=True)
    except telebot.apihelper.ApiTelegramException as e:
        if "Too Many Requests" in str(e):
            time_to_wait = int(str(e).split("retry after ")[1].split()[0])
            check_subscription(call)  # Կրկին փորձում ենք ստուգել բաժանորդագրությունը
        else:
            bot.answer_callback_query(call.id, "Չհաջողվեց ստուգել բաժանորդագրությունը:", show_alert=True)
            print(e)


if __name__ == "__main__":
    bot.infinity_polling(none_stop=True, interval=0.5)
