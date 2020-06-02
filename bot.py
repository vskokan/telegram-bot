from telegram.ext import Updater, MessageHandler
from telegram.ext import Filters
from telegram import Sticker
from telegram import KeyboardButton
from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler
import postgres
import myparser
from telegram import User
from telegram import Message
import apiai, json

# Bot connection
REQUEST_KWARGS = {
    'proxy_url': 'socks5://138.201.153.200:1080',
}
updater = Updater(token='', use_context=True,
                  request_kwargs=REQUEST_KWARGS)
dispatcher = updater.dispatcher

# Import logs
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# Connection to database and creation tables for content and user state
con = postgres.con
postgres.create_table_for_state(con)
postgres.create_table(con)


# Initialization of variables (may be useless...)
username = 'undefined'
user_info = 'undefined'
user_state = 'undefined'
user_id = 'undefined'

# Functions

# Reset user state (same as start but without greeting)
def reset(update, context): 
    user_id = update.message.from_user.id
    user_state = 'initial'
    postgres.reset_user_state(con, current_id=user_id) 
    postgres.init_state(con, current_id=user_id,state=user_state)
    message = 'Сброс выполнен'
    update.message.reply_text(message, reply_markup=my_keyboard)

# Init user state
def start(update, context):
    global user_id
    user_id = update.message.from_user.id
    user = update.message.from_user
    global username
    username=user.first_name
    message='Привет, '+ username
    global user_state
    user_state = 'initial'
    postgres.reset_user_state(con, current_id=user_id) 
    postgres.init_state(con, current_id=user_id,state=user_state)
    update.message.reply_text(message, reply_markup=my_keyboard)

# Print help info
def help(update, context): 
    context.bot.send_message(chat_id=update.effective_chat.id, text=str(postgres.get_message(con, tag="help")))

# View all items of all categories for current user 
def viewall(update, context):
    user_id = update.message.from_user.id
    if not postgres.has_something(con, current_id=user_id, category='all'):
        context.bot.send_message(chat_id=update.effective_chat.id, text='Пусто...')
    else:
        dbtext = postgres.get_all_data(con, current_id=user_id)
        contentlist = postgres.representate_data(dbtext) 
        text = ''.join(contentlist) 
        context.bot.send_message(chat_id=update.effective_chat.id, text=text)

# View items of specific category for current user
def view_items(update, context, category):
    user_id = update.message.from_user.id
    if not postgres.has_something(con, current_id=user_id, category=category):
        context.bot.send_message(chat_id=update.effective_chat.id, text='Пусто...')
    else:
        dbtext = postgres.get_items(con, current_id=user_id, category=category)
        contentlist = postgres.representate_data(dbtext)
        text = ''.join(contentlist)
        context.bot.send_message(chat_id=update.effective_chat.id, text=text)

# View random item of specific category for current user
def random_item(update, context, category):
    user_id = update.message.from_user.id
    if not postgres.has_something(con, current_id=user_id, category=category):
        context.bot.send_message(chat_id=update.effective_chat.id, text='Пусто...')
    else:
        text = postgres.get_random_item(con, current_id=user_id, category=category) 
        text = text + '\n' + postgres.get_message(con, tag="notification") 
        context.bot.send_message(chat_id=update.effective_chat.id, text=text)

# Define category of item which will be deleted by asking user
def define_category(update, context, name):
    context.bot.send_message(chat_id=update.effective_chat.id, text = postgres.get_message(con, tag="del_concidence"))
    user_id = update.message.from_user.id
    postgres.update_state(con, current_id=user_id, state = 'defines category')

# Deletion by item name (category will be received from function define category)
def delete_by_name_only(update, context, text):
    category = myparser.parse_category(update.message.text)
    context.bot.send_message(chat_id=update.effective_chat.id, text = 'Удалено: '+ category + ' ' + text + '.') 
    user_id = update.message.from_user.id
    dbdata = (user_id, category, text)
    postgres.delete_by_name_and_category(con, dbdata)
    postgres.update_state(con, current_id=user_id, state = 'initial')

# Processing user messages when user state is initial
def text_processing(update, context, text):
    if text.startswith('Привет') or text.startswith('привет'):
        return start(update=update, context=context)
    elif myparser.parse_category(text):
        category = myparser.parse_category(text)
        return view_items(update, context, category=category) 
    elif text == 'Всё вместе':
        return viewall(update=update, context=context)
    elif text == 'Помощь':
        return help(update=update, context=context)
    elif text == 'Давай пообщаемся':
        update.message.reply_text(text="Давай! Напиши мне что-нибудь!", reply_markup=smalltalk_keyboard)
        user_id = update.message.from_user.id
        postgres.update_state(con, current_id=user_id, state = 'wants to talk')
    elif myparser.parse_query_to_random_item(text):
        category = myparser.parse_query_to_random_item(text)
        return random_item(update, context, category=category)
    elif myparser.parse_insertion(text):
        category, name = myparser.parse_insertion(text)
        current_id = update.message.from_user.id
        dbdata = (name, current_id, category)
        if  postgres.is_already_exists(con, dbdata):
            text = postgres.get_message(con, tag="ins_concidence")
            update.message.reply_text(text=text, reply_markup=my_keyboard)
        else:  
            dbdata = (current_id, category, name)
            postgres.insert_in_db(con,dbdata=dbdata)
            update.message.reply_text(text=update.message.text + postgres.get_message(con, tag='ins_success'), reply_markup=my_keyboard)
    elif myparser.parse_deletion_by_name_only(text):
        current_id = update.message.from_user.id
        name = myparser.parse_deletion_by_name_only(text)
        if postgres.find_match_in_db(con, name) == 1:
            dbdata = (current_id, name)
            postgres.delete_by_name(con, dbdata)
            update.message.reply_text(text=name + postgres.get_message(con, tag="del_success"), reply_markup=my_keyboard)
        else:
            global temp
            temp = name
            print(name)
            print(temp)
            define_category(update=update, context=context, name=temp)
    elif myparser.parse_deletion(text):
        current_id = update.message.from_user.id
        category, name = myparser.parse_deletion(text)
        dbdata = (current_id, category, name)
        postgres.delete_by_name_and_category(con, dbdata=dbdata)
        update.message.reply_text(text=category +' '+ name + postgres.get_message(con, tag="del_success"),reply_markup=my_keyboard)
    elif 'initial' == postgres.get_state(con, current_id=update.message.from_user.id):
        update.message.reply_text(text=postgres.get_message(con, tag="not_recognized_text"), reply_markup=my_keyboard)

# Useless function for response on sended images
def image_processing(update, context): 
    context.bot.send_message(chat_id=update.effective_chat.id, text = 'Я не умею распознавать картинки...')

# Function for working with Dialogflow
def small_talk(update, context):
    request = apiai.ApiAI('a288b1e5ef9e44f791defd9cad6a639b ').text_request()
    request.lang = 'ru' 
    request.session_id = 'vmvBot' 
    request.query = update.message.text
    responseJson = json.loads(request.getresponse().read().decode('utf-8'))
    response = responseJson['result']['fulfillment']['speech']
    if response:
        context.bot.send_message(chat_id=update.message.chat_id, text=response)
    else:
        context.bot.send_message(chat_id=update.message.chat_id, text=postgres.get_message(con, tag="not_recognized_text"))

# Defines what function will be returned in dependence of user state
def user_state_processing(update, context):
    state = postgres.get_state(con, current_id=update.message.from_user.id)
    text = update.message.text
    if state == 'initial':
        return text_processing(update=update, context=context, text=text)
    if state == 'defines category':
        return delete_by_name_only(update=update, context=context, text=temp)
    if state == 'wants to talk':
        return small_talk(update=update, context=context)

# Keyboard
button_start=KeyboardButton('/start')
button_help=KeyboardButton('Помощь')
button_viewall=KeyboardButton('Всё вместе')
button_viewbooks=KeyboardButton('Книги')
button_viewfilms=KeyboardButton('Фильмы')
button_randomfilm=KeyboardButton('Что посмотреть?')
button_randombook=KeyboardButton('Что почитать?')
button_exit=KeyboardButton('/reset')
button_smalltalk=KeyboardButton('Давай пообщаемся')

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
        [
            button_smalltalk,
        ], 
    ],
    resize_keyboard=True,
)

smalltalk_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            button_exit,
        ],
        [
        ],
    ],
    resize_keyboard=True,
)

# Handlers
start_handler = CommandHandler('start', start)
help_handler = CommandHandler('help', help)
viewall_handler = CommandHandler('viewall', viewall)
reset_handler = CommandHandler('reset', reset)
small_talk_handler = CommandHandler('smalltalk', small_talk)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(help_handler)
dispatcher.add_handler(viewall_handler)
dispatcher.add_handler(reset_handler)
dispatcher.add_handler(MessageHandler(filters=Filters.text, callback=user_state_processing))
dispatcher.add_handler(MessageHandler(filters=Filters.photo, callback=image_processing))
updater.start_polling()
