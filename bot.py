from telegram.ext import Updater, MessageHandler
from telegram.ext import Filters
from telegram import Sticker
from telegram import KeyboardButton
from telegram import ReplyKeyboardMarkup
REQUEST_KWARGS = {
    'proxy_url': 'socks5://82.223.120.213:1080',
}
updater = Updater(token='1189380390:AAGtbHYKIv_HDlGy4qyaOQ3ukB2GNyY_osE', use_context=True,
                  request_kwargs=REQUEST_KWARGS)
dispatcher = updater.dispatcher
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def start(update, context):
    context.bot.send_sticker(chat_id=update.effective_chat.id, sticker='CAACAgIAAxkBAAJEgV6S3HULh2rF6FWtQp1jbx4BgQmzAAI4BAAC6VUFGLPOVS1ipdVcGAQ')
    message='Привет!'
    update.message.reply_text(message, reply_markup=my_keyboard)

def help(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Потом здесь будет список доступных команд и прочее....")

def bye(update, context):
    context.bot.send_sticker(chat_id=update.effective_chat.id, sticker='CAACAgIAAxkBAAJEg16S3LxeZFxpW6pAe6AX9dY4a33ZAAJIBAAC6VUFGH2PWbP4cz4cGAQ')
    context.bot.send_message(chat_id=update.effective_chat.id, text="Пока 😔")

def who_are_you(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Я - бот")
    context.bot.send_sticker(chat_id=update.effective_chat.id, sticker='CAACAgIAAxkBAAJEll6S61cD-mDbCFfBLgXREpJ1k9JNAAIqBAAC6VUFGJ9J7Vm07rMyGAQ')
    

def text_message_processing(update, context):
    text = update.message.text
    if text == 'Кто ты?':
        return who_are_you(update=update, context=context)

    update.message.reply_text(
        text="Я не умею распознавать такой текст...пока что!",
        reply_markup=my_keyboard,
    )

def image_processing(update, context):
    context.bot.send_sticker(chat_id=update.effective_chat.id, sticker='CAACAgIAAxkBAAJEf16S3Dp5mjWXu0NdIbqRft87tfQHAAI7BAAC6VUFGON-fsJ0gbtJGAQ')
    context.bot.send_message(chat_id=update.effective_chat.id, text = 'Я не умею распознавать картинки...')

from telegram.ext import CommandHandler

button_start=KeyboardButton('/start')
button_help=KeyboardButton('/help')
button_bye=KeyboardButton('/bye')
my_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            button_start,
            button_help,
            button_bye,
        ],     
    ],
    resize_keyboard=True,
)

start_handler = CommandHandler('start', start)
bye_handler = CommandHandler('bye', bye)
help_handler = CommandHandler('help', help)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(bye_handler)
dispatcher.add_handler(help_handler)
dispatcher.add_handler(MessageHandler(filters=Filters.text, callback=text_message_processing))
dispatcher.add_handler(MessageHandler(filters=Filters.photo, callback=image_processing))
updater.start_polling()
