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
    'proxy_url': 'socks5://82.223.120.213:1080',
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

def viewbooks(update, context):
    current_id = update.message.from_user.id
    dbtext = sqlmodule.get_books(con, current_id=current_id)
    contentlist = sqlmodule.representate_data(dbtext)
    text = ''.join(contentlist)
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)

def viewfilms(update, context):
    current_id = update.message.from_user.id
    dbtext = sqlmodule.get_films(con, current_id=current_id)
    contentlist = sqlmodule.representate_data(dbtext)
    text = ''.join(contentlist)
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)

def who_are_you(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Я - бот")
    context.bot.send_sticker(chat_id=update.effective_chat.id, sticker='CAACAgIAAxkBAAJEll6S61cD-mDbCFfBLgXREpJ1k9JNAAIqBAAC6VUFGJ9J7Vm07rMyGAQ')
    
def text_message_processing(update, context):
    text = update.message.text
    if text == 'Кто ты?':
        return who_are_you(update=update, context=context)

    if myparser.parseInsertion(text):
        category, name = myparser.parseInsertion(text)
        current_id = update.message.from_user.id
        #current_chat = update.effective_chat.id
        dbdata = (current_id, category, name)
        sqlmodule.insert_in_db(con,dbdata=dbdata)
        update.message.reply_text(
            text=update.message.text + " - " + "внесено в базу данных!",
            reply_markup=my_keyboard,
        )
    elif myparser.parseDeletion(text):
        current_id = update.message.from_user.id
        name = myparser.parseDeletion(text)
        entranceAmount = sqlmodule.find_match_in_db(con, name=name)[0]
        #print(sqlmodule.find_match_in_db(con, name=name))
        if entranceAmount[0] > 1:
            ask_about_category(update=update, context=context)
            parsed_category = enter_category(update=update, context=context)
            if parsed_category != 0:
                category = parsed_category
                dbdata = (current_id, category, name)
                sqlmodule.delete_by_name_and_category(con, dbdata=dbdata)
            else:
                pass
        else:
            dbdata = (current_id, name)
            sqlmodule.delete_by_name(con, dbdata=dbdata)
            update.message.reply_text(
            text="Удалено!",
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

# НЕ РАБОТАЕТ В СЛУЧАЕ, ЕСЛИ ЕСТЬ СОВПАДЕНИЯ! 

def ask_about_category(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text = 'Книга или фильм?')
    text = update.message.text
    if text.startswith("Фильм ") or text.startswith("фильм ") or text.startswith("Книга ") or text.startswith("книга "):
        context.bot.send_message(chat_id=update.effective_chat.id, text = 'Хммм')
        return text    
    #context.bot.register_next_step_handler(msg, enter_category)

def enter_category(update, context):
    text = update.message.text
    if text.startswith("Фильм ") or text.startswith("фильм ") or text.startswith("Книга ") or text.startswith("книга "):
        context.bot.send_message(chat_id=update.effective_chat.id, text = 'Хммм')
        return text    

button_start=KeyboardButton('/start')
button_help=KeyboardButton('/help')
button_bye=KeyboardButton('/bye')
button_viewall=KeyboardButton('/viewall')
button_viewbooks=KeyboardButton('/viewbooks')
button_viewfilms=KeyboardButton('/viewfilms')
my_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            button_start,
            button_help,
            button_bye,
            button_viewall,
            button_viewbooks,
            button_viewfilms,
        ],     
    ],
    resize_keyboard=True,
)

start_handler = CommandHandler('start', start)
bye_handler = CommandHandler('bye', bye)
help_handler = CommandHandler('help', help)
viewall_handler = CommandHandler('viewall', viewall)
viewbooks_handler = CommandHandler('viewbooks', viewbooks)
viewfilms_handler = CommandHandler('viewfilms', viewfilms)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(bye_handler)
dispatcher.add_handler(help_handler)
dispatcher.add_handler(viewall_handler)
dispatcher.add_handler(viewbooks_handler)
dispatcher.add_handler(viewfilms_handler)
dispatcher.add_handler(MessageHandler(filters=Filters.text, callback=text_message_processing))
dispatcher.add_handler(MessageHandler(filters=Filters.photo, callback=image_processing))
updater.start_polling()
