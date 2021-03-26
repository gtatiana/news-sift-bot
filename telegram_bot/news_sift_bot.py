import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
import telegram_bot.constant
from storage.pg_storage import PGStorage

bot = telebot.TeleBot(telegram_bot.constant.TELEGRAM_TOKEN)
storage = PGStorage(telegram_bot.constant.DATABASE_DSN)


def get_article_links(is_positive):
    return storage.get_article_links(is_positive)


def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton('Positive', callback_data='news_pos'),
               InlineKeyboardButton('Negative', callback_data='news_neg'))
    return markup


@bot.callback_query_handler(func=lambda call: call.data.startswith('news_pos'))
def get_positive_news(call):
    links = get_article_links(1)
    for link in links:
        bot.send_message(chat_id=call.message.chat.id, text=link)
    bot.send_message(call.message.chat.id, telegram_bot.constant.QUESTION, reply_markup=gen_markup())


@bot.callback_query_handler(func=lambda call: call.data.startswith('news_neg'))
def get_negative_news(call):
    links = get_article_links(0)
    for link in links:
        bot.send_message(chat_id=call.message.chat.id, text=link)
    bot.send_message(call.message.chat.id, telegram_bot.constant.QUESTION, reply_markup=gen_markup())


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, telegram_bot.constant.WELCOME_MESSAGE)
    bot.send_message(message.chat.id, telegram_bot.constant.QUESTION, reply_markup=gen_markup())


def run_bot():
    bot.polling(none_stop=True)
