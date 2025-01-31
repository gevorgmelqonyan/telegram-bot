import time
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

API_TOKEN = "8016439844:AAGrDy-2KjhWYQPAzgDUAUEz13ujvAKWPoU"
CHANNEL_USERNAME = "@WalkersMadrid"

link = {"link": "https://liveball.uno/match/1299124"}

bot = telebot.TeleBot(API_TOKEN)

def create_start_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    subscribe_button = KeyboardButton("🔔 Բաժանորդագրվել")
    check_subscription_button = KeyboardButton("✅ Ստանալ հղումը")
    keyboard.add(subscribe_button, check_subscription_button)
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
    link["link"] = message.text.split("-", 1)[1]

@bot.message_handler(func=lambda message: message.text == "✅ Ստանալ հղումը")
def check_subscription(message):
    user_id = message.from_user.id
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        if member.status in ["member", "administrator", "creator"]:
            msg = bot.send_message(message.chat.id, text=link["link"])
            time.sleep(60)
            bot.delete_message(message.chat.id, msg.message_id)
        else:
            bot.send_message(message.chat.id, "Դուք բաժանորդագրված չեք ալիքին, բաժանորդագրվեք հղումը ստանալու համար")
    except Exception as e:
        bot.send_message(message.chat.id, "Չհաջողվեց ստուգել բաժանորդագրությունը:")
        print(e)

if __name__ == "__main__":
    bot.infinity_polling(none_stop=True)
