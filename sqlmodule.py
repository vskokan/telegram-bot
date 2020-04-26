import sqlite3
from sqlite3 import Error
import random
from kinopoisk.movie import Movie
import wikipedia

con = sqlite3.connect('botcontent.db',  check_same_thread=False)

def db_connection():
    try:
        con = sqlite3.connect('botcontent.db',  check_same_thread=False)
        return con
    except Error:
        print(Error)

def create_table(con):
    cursor_obj = con.cursor()
    cursor_obj.execute("CREATE TABLE IF NOT EXISTS content(id integer PRIMARY KEY, user_id text, category text, name text)")
    con.commit()

def insert_in_db(con, dbdata):
    cursor_obj = con.cursor()
    cursor_obj.execute('''INSERT INTO content(user_id, category, name) VALUES(?, ?, ?)''', dbdata)
    con.commit()

def get_all_data(con, current_id):
    cursor_obj = con.cursor()
    cursor_obj.execute("SELECT category, name FROM content WHERE user_id=?", (current_id,))
    rows = cursor_obj.fetchall()
    return rows

def representate_data(dbdata):
    datalist_length = len(dbdata)
    print(datalist_length)
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
    cursor_obj.execute("SELECT category, name FROM content WHERE user_id=? AND category=?", (current_id, category))
    rows = cursor_obj.fetchall()
    return rows   

def find_match_in_db(con, name): #на будущее
    cursor_obj = con.cursor()
    cursor_obj.execute("SELECT COUNT(*) FROM content WHERE name=?", (name,))
    items_amount = cursor_obj.fetchall()
    return items_amount

def delete_by_name_and_category(con, dbdata):
    cursor_obj = con.cursor()
    cursor_obj.execute("DELETE FROM content WHERE user_id=? AND category=? AND name=?", dbdata)
    con.commit()    

def delete_by_name(con, dbdata): #на будущее
    cursor_obj = con.cursor()
    cursor_obj.execute("DELETE FROM content WHERE user_id=? AND name=?", dbdata)
    con.commit()   

def get_random_item(con, current_id, category):
    cursor_obj = con.cursor()
    cursor_obj.execute("SELECT name FROM content WHERE user_id=? AND category=?  ORDER BY random() LIMIT 1", (current_id, category))
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
                        link+="🔎" + str(movie_list[index].title) + " / " + str(movie_list[index].title_en) +"\n"+"https://www.kinopoisk.ru/film/" + str(movie_list[index].id) + "/" + "\n Cнято в:  " + str(movie_list[index].year) +'\n Рейтинг: ' + str(movie_list[index].rating) +'\n'
                index+=1
            if link == "":
                link = "\nКажется, не нашлось ничего вызывающего доверие (не рассматриваю фильмы с рейтингом ниже 7) или просто ничего не нашлось 😕"
    answers = ['Как насчет этого?🤔', 'Держи', 'Как тебе такое?', '🤔Может..?']
    datastring = answers[random.randint(0, len(answers)-1)] + '\n' + emoji + str((random_item[0])[0])+'\n'+"Вот что мне удалось найти: \n" + link
    return datastring

def is_already_exists(con, dbdata):
    cursor_obj = con.cursor()
    cursor_obj.execute("SELECT COUNT(*) FROM content WHERE name=? AND user_id=? AND category=?", dbdata)
    item = cursor_obj.fetchall()
    amount = item[0][0]
    if amount==0:
        return 0
    else:
        return 1