from telegram.ext import Updater, MessageHandler
from telegram.ext import Filters
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

button_help = 'Тык'


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Приветик")



def bye(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Пока ((")
    updater.stop()


def message_processing(update, context):

    reply_markup = ReplyKeyboardMarkup(
       keyboard=[
            [
                KeyboardButton(text=button_help)
            ],
        ],
        resize_keyboard=True,
    )
    update.message.reply_text(
        text="здесь что-то будет",
        reply_markup=reply_markup,
    )


from telegram.ext import CommandHandler

start_handler = CommandHandler('start', start)
bye_handler = CommandHandler('bye', bye)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(bye_handler)
dispatcher.add_handler(MessageHandler(filters=Filters.text, callback=message_processing))
updater.start_polling()