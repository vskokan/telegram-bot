import random
from kinopoisk.movie import Movie
import wikipedia

import psycopg2
from psycopg2 import Error

con = psycopg2.connect("dbname=dd2j0v3o62h71a user=xbpjvzpfpwvifd password=0dd64fb73d4b8d3aca46e795d24b9bb24486eb5231e45e361c4d7d7fbf282ad6 host=ec2-54-246-90-10.eu-west-1.compute.amazonaws.com")

# User state

def create_table_for_state(con):
    cursor_obj = con.cursor()
    cursor_obj.execute("CREATE TABLE IF NOT EXISTS user_state (user_id integer PRIMARY KEY, state text)")
    con.commit()

create_table_for_state(con)

def init_state(con, current_id, state):
    cursor_obj = con.cursor()
    cursor_obj.execute("INSERT INTO user_state (user_id, state) VALUES(%s, %s)", (current_id, state,))
    con.commit()

def update_state(con, current_id, state):
    cursor_obj = con.cursor()
    cursor_obj.execute("UPDATE user_state SET state = %s WHERE user_id = %s", (state, current_id, ))
    con.commit()

def get_state(con, current_id):
    cursor_obj = con.cursor()
    cursor_obj.execute("SELECT state FROM user_state WHERE user_id = %s", (current_id,))
    state = cursor_obj.fetchall()
    return state[0][0]

def reset_user_state(con, current_id):
    cursor_obj = con.cursor()
    cursor_obj.execute("DELETE FROM user_state WHERE user_id = %s", (current_id,))
    con.commit()

# Working with content

def create_table(con):
    cursor_obj = con.cursor()
    cursor_obj.execute("CREATE TABLE IF NOT EXISTS content(id serial PRIMARY KEY, user_id integer, category text, name text)")
    con.commit()

def insert_in_db(con, dbdata):
    cursor_obj = con.cursor()
    cursor_obj.execute("INSERT INTO content(user_id, category, name) VALUES(%s, %s, %s)", dbdata)
    con.commit()

def get_all_data(con, current_id):
    cursor_obj = con.cursor()
    cursor_obj.execute("SELECT category, name FROM content WHERE user_id = %s", (current_id,))
    rows = cursor_obj.fetchall()
    return rows

def representate_data(dbdata):
    datalist_length = len(dbdata)
    datalist = []
    index = 1
    while index < datalist_length + 1:
        tempdata = dbdata[index-1]
        if tempdata[0] == 'Книга':
            emoji = '📚'
        else:
            emoji = '🎬'
        datastring = str(index) + '. ' + emoji + str(tempdata[1])+'\n'
        datalist.append(datastring)
        index = index + 1
    return datalist

def get_items(con, current_id, category):
    cursor_obj = con.cursor()
    cursor_obj.execute("SELECT category, name FROM content WHERE user_id = %s AND category = %s", (current_id, category))
    rows = cursor_obj.fetchall()
    return rows   

def find_match_in_db(con, name): 
    cursor_obj = con.cursor()
    cursor_obj.execute("SELECT COUNT(*) FROM content WHERE name = %s", (name,))
    items_amount = cursor_obj.fetchall()
    return items_amount[0][0]

def delete_by_name_and_category(con, dbdata):
    cursor_obj = con.cursor()
    cursor_obj.execute("DELETE FROM content WHERE user_id = %s AND category = %s AND name = %s", dbdata)
    con.commit()    

def delete_by_name(con, dbdata): 
    cursor_obj = con.cursor()
    cursor_obj.execute("DELETE FROM content WHERE user_id = %s AND name = %s", dbdata)
    con.commit()   

def get_random_item(con, current_id, category):
    cursor_obj = con.cursor()
    cursor_obj.execute("SELECT name FROM content WHERE user_id = %s AND category = %s ORDER BY random() LIMIT 1", (current_id, category))
    random_item = cursor_obj.fetchall()
    if category == 'Книга':
            emoji = '📚'
            wikipedia.set_lang("ru")
            link =str(wikipedia.page(str((random_item[0])[0])).url)
    else:
            emoji = '🎬'
            movie_list = Movie.objects.search(str((random_item[0])[0]))
            link = ""
            index = 0
            while index < len(movie_list)  and index < 5:
                if str(movie_list[index].rating) !='None':
                    if movie_list[index].rating > 7:
                        link+="🔎" + str(movie_list[index].title) + " / " + str(movie_list[index].title_en) + "\n Cнято в: " + str(movie_list[index].year) +'\n Рейтинг: ' + str(movie_list[index].rating) +'\n' + "Ссылки на кипопоиск пока недоступны 😔"
                index+=1
            if link == "":
                link = "\nКажется, на Кинопоиске не нашлось ничего вызывающего доверие (не рассматриваю фильмы с рейтингом ниже 7 ) или просто ничего не нашлось 😕"
    answers = ['Как насчет этого?🤔', 'Держи', 'Как тебе такое?', '🤔Может..?']
    datastring = answers[random.randint(0, len(answers)-1)] + '\n' + emoji + str((random_item[0])[0])+'\n'+"Вот что мне удалось найти: \n" + link
    return datastring

def is_already_exists(con, dbdata):
    cursor_obj = con.cursor()
    cursor_obj.execute("SELECT COUNT(*) FROM content WHERE name= %s AND user_id = %s AND category = %s", dbdata)
    item = cursor_obj.fetchall()
    amount = item[0][0]
    if amount==0:
        return 0
    else:
        return 1

def has_something(con, current_id, category):
    cursor_obj = con.cursor()
    if category == 'all':
        cursor_obj.execute("SELECT COUNT(*) FROM content WHERE user_id = %s", (current_id,))
        amount = cursor_obj.fetchall()
    else:
        cursor_obj.execute("SELECT COUNT(*) FROM content WHERE user_id = %s AND category = %s", (current_id, category,))
        amount = cursor_obj.fetchall()  
    return amount[0][0]

# Function for getting messages 
def get_message(con, tag):
    cursor_obj = con.cursor()
    cursor_obj.execute("SELECT message FROM messages WHERE tag = %s", (tag,))
    message = cursor_obj.fetchall()
    return str((message[0])[0])
