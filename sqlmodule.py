import sqlite3
from sqlite3 import Error
import random

con = sqlite3.connect('botcontent.db',  check_same_thread=False)

def db_connection():
    try:
        con = sqlite3.connect('botcontent.db',  check_same_thread=False)
        return con
    except Error:
        print(Error)

def create_table(con):
    cursorObj = con.cursor()
    cursorObj.execute("CREATE TABLE IF NOT EXISTS content(id integer PRIMARY KEY, user_id text, category text, name text)")
    con.commit()

def insert_in_db(con, dbdata):
    cursorObj = con.cursor()
    cursorObj.execute('''INSERT INTO content(user_id, category, name) VALUES(?, ?, ?)''', dbdata)
    con.commit()

def get_all_data(con, current_id):
    cursorObj = con.cursor()
    cursorObj.execute("SELECT category, name FROM content WHERE user_id=?", (current_id,))
    rows = cursorObj.fetchall()
    for row in rows:
        print (row)
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
        print (datastring)
        index = index + 1
    return datalist

def get_items(con, current_id, category):
    cursorObj = con.cursor()
    cursorObj.execute("SELECT category, name FROM content WHERE user_id=? AND category=?", (current_id, category))
    rows = cursorObj.fetchall()
    for row in rows:
        print (row)
    return rows   

def find_match_in_db(con, name):
    cursorObj = con.cursor()
    cursorObj.execute("SELECT COUNT(*) FROM content WHERE name=?", (name,))
    items_amount = cursorObj.fetchall()
    return items_amount

def delete_by_name_and_category(con, dbdata):
    cursorObj = con.cursor()
    cursorObj.execute("DELETE FROM content WHERE user_id=? AND category=? AND name=?", dbdata)
    con.commit()    

def delete_by_name(con, dbdata):
    cursorObj = con.cursor()
    cursorObj.execute("DELETE FROM content WHERE user_id=? AND name=?", dbdata)
    con.commit()   

def get_random_item(con, current_id, category):
    cursorObj = con.cursor()
    cursorObj.execute("SELECT name FROM content WHERE user_id=? AND category=?  ORDER BY random() LIMIT 1", (current_id, category))
    random_item = cursorObj.fetchall()
    if category == 'Книга':
            emoji = '📚'
    else:
            emoji = '🎬'
    answers = ['Как насчет этого?🤔', 'Держи', 'Как тебе такое?', '🤔Может..?']
    datastring = answers[random.randint(0, len(answers)-1)] + '\n' + emoji + str((random_item[0])[0])+'\n'
    return datastring

