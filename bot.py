from telegram.ext import Updater, MessageHandler
from telegram.ext import Filters
from telegram import Sticker
from telegram import KeyboardButton
from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler
import sqlmodule
import myparser
from telegram import User
from telegram import Message

REQUEST_KWARGS = {
    'proxy_url': 'socks5://148.251.234.93:1080',
}
updater = Updater(token='1189380390:AAGtbHYKIv_HDlGy4qyaOQ3ukB2GNyY_osE', use_context=True,
                  request_kwargs=REQUEST_KWARGS)
dispatcher = updater.dispatcher
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

con = sqlmodule.con
sqlmodule.create_table(con)
answer_category = True

def start(update, context):
    #context.bot.send_sticker(chat_id=update.effective_chat.id, sticker='CAACAgIAAxkBAAJEgV6S3HULh2rF6FWtQp1jbx4BgQmzAAI4BAAC6VUFGLPOVS1ipdVcGAQ')
    user = update.message.from_user
    message='Привет, '+ user.first_name
    update.message.reply_text(message, reply_markup=my_keyboard)

def help(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Потом здесь будет список доступных команд и прочее....")

def bye(update, context):
    context.bot.send_sticker(chat_id=update.effective_chat.id, sticker='CAACAgIAAxkBAAJEg16S3LxeZFxpW6pAe6AX9dY4a33ZAAJIBAAC6VUFGH2PWbP4cz4cGAQ')
    context.bot.send_message(chat_id=update.effective_chat.id, text="Пока 😔")

def viewall(update, context):
    current_id = update.message.from_user.id
    dbtext = sqlmodule.get_all_data(con, current_id=current_id)
    contentlist = sqlmodule.representate_data(dbtext)
    text = ''.join(contentlist)
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)

def view_items(update, context, category):
    current_id = update.message.from_user.id
    dbtext = sqlmodule.get_items(con, current_id=current_id, category=category)
    contentlist = sqlmodule.representate_data(dbtext)
    text = ''.join(contentlist)
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)

def random_item(update, context, category):
    current_id = update.message.from_user.id
    text = sqlmodule.get_random_item(con, current_id=current_id, category=category) 
    text = text + '\nНе забудь сообщить мне, когда ознакомишься с этим!'
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)

def who_are_you(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Я - бот")
    context.bot.send_sticker(chat_id=update.effective_chat.id, sticker='CAACAgIAAxkBAAJEll6S61cD-mDbCFfBLgXREpJ1k9JNAAIqBAAC6VUFGJ9J7Vm07rMyGAQ')
    
def text_message_processing(update, context):
    text = update.message.text
    if text == 'Кто ты?':
        return who_are_you(update=update, context=context)
    elif text.startswith('Привет') or text.startswith('привет'):
        return start(update=update, context=context)
    elif text == 'Фильмы' or text == 'фильмы':
        category = 'Фильм'
        return view_items(update, context, category=category)    
    elif text == 'Книги' or text == 'книги':
        category = 'Книга'
        return view_items(update, context, category=category) 
    elif text == 'Всё вместе':
        return viewall(update=update, context=context)
    elif text == 'Помощь':
        return help(update=update, context=context)
    elif text.startswith('Что посмотреть') or text.startswith('что посмотреть') or text.startswith('посмотреть') or text.startswith('Посмотреть'):
        category = 'Фильм'
        return random_item(update, context, category=category)
    elif text.startswith('Что почитать') or text.startswith('что почитать') or text.startswith('почитать') or text.startswith('Почитатьь'):
        category = 'Книга'
        return random_item(update, context, category=category)
    elif myparser.parseInsertion(text):
        category, name = myparser.parseInsertion(text)
        current_id = update.message.from_user.id
        dbdata = (current_id, category, name)
        sqlmodule.insert_in_db(con,dbdata=dbdata)
        update.message.reply_text(
            text=update.message.text + " - " + "внесено в базу данных!",
            reply_markup=my_keyboard,
        )
    elif myparser.parseDeletion(text):
        current_id = update.message.from_user.id
        category, name = myparser.parseDeletion(text)
        dbdata = (current_id, category, name)
        sqlmodule.delete_by_name_and_category(con, dbdata=dbdata)
        update.message.reply_text(
            text=category +' '+ name + " - " + "удалено из базы данных!",
            reply_markup=my_keyboard,
        )
    else:
        update.message.reply_text(
            text="Не понял",
            reply_markup=my_keyboard,
        )

def image_processing(update, context):
    context.bot.send_sticker(chat_id=update.effective_chat.id, sticker='CAACAgIAAxkBAAJEf16S3Dp5mjWXu0NdIbqRft87tfQHAAI7BAAC6VUFGON-fsJ0gbtJGAQ')
    context.bot.send_message(chat_id=update.effective_chat.id, text = 'Я не умею распознавать картинки...')
 
button_start=KeyboardButton('/start')
button_help=KeyboardButton('Помощь')
button_viewall=KeyboardButton('Всё вместе')
button_viewbooks=KeyboardButton('Книги')
button_viewfilms=KeyboardButton('Фильмы')
button_randomfilm=KeyboardButton('Что посмотреть?')
button_randombook=KeyboardButton('Что почитать?')
my_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            
            button_viewbooks,
            button_viewfilms,
            button_viewall,
        ],  
        [
            button_randomfilm,
            button_randombook,
        ],  
        [
            button_help,
        ], 
    ],
    resize_keyboard=True,
)

start_handler = CommandHandler('start', start)
help_handler = CommandHandler('help', help)
viewall_handler = CommandHandler('viewall', viewall)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(help_handler)
dispatcher.add_handler(viewall_handler)
dispatcher.add_handler(MessageHandler(filters=Filters.text, callback=text_message_processing))
dispatcher.add_handler(MessageHandler(filters=Filters.photo, callback=image_processing))
updater.start_polling()
