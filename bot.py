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
    'proxy_url': 'socks5://5.133.217.88:4249',
}
updater = Updater(token='1189380390:AAGtbHYKIv_HDlGy4qyaOQ3ukB2GNyY_osE', use_context=True,
                  request_kwargs=REQUEST_KWARGS)
dispatcher = updater.dispatcher
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

con = sqlmodule.con
sqlmodule.create_table(con)

def start(update, context):
    user = update.message.from_user
    message='Привет, '+ user.first_name
    update.message.reply_text(message, reply_markup=my_keyboard)

def help(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="📍Чтобы внести фильм или книгу в базу данных бота, напиши сообщение следующего формата: фильм/книга Название \n Например, фильм Властелин Колец. Категорию можно писать и с большой буквы!  \n 📍Чтобы удалить запись, достаточно написать: прочитано/просмотрено или посмотрел(а)/прочитал(а) и название через пробел \nНапример, посмотрел Властелин Колец  \n📍С помощью кнопок на клавиатуре бота можно просмотреть, что было внесено, по категориям или все вместе  \n📍Список команд:  \n/help \n/viewall \n")

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
    text = text + '\nНе забудь сообщить мне, когда ознакомишься с этим, либо просто решишь удалить'
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
    elif myparser.parse_category(text):
        category = myparser.parse_category(text)
        return view_items(update, context, category=category) 
    elif text == 'Всё вместе':
        return viewall(update=update, context=context)
    elif text == 'Помощь':
        return help(update=update, context=context)
    elif myparser.parse_query_to_random_item(text):
        category = myparser.parse_query_to_random_item(text)
        return random_item(update, context, category=category)
    elif myparser.parse_insertion(text):
        category, name = myparser.parse_insertion(text)
        current_id = update.message.from_user.id
        dbdata = (name, current_id, category)
        if  sqlmodule.is_already_exists(con, dbdata):
            update.message.reply_text(
                text="Кажется, это уже было внесено...",
                reply_markup=my_keyboard,
            )
        else:  
            dbdata = (current_id, category, name)
            sqlmodule.insert_in_db(con,dbdata=dbdata)
            update.message.reply_text(
            text=update.message.text + " - " + "внесено в базу данных!",
            reply_markup=my_keyboard,
            )
    elif myparser.parse_deletion(text):
        current_id = update.message.from_user.id
        category, name = myparser.parse_deletion(text)
        dbdata = (current_id, category, name)
        sqlmodule.delete_by_name_and_category(con, dbdata=dbdata)
        update.message.reply_text(
            text=category +' '+ name + " - " + "удалено из базы данных!",
            reply_markup=my_keyboard,
        )
    else:
        update.message.reply_text(
            text="Не понимаю...",
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
