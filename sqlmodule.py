import sqlite3
from sqlite3 import Error

con = sqlite3.connect('botcontent.db',  check_same_thread=False)

def db_connection():
    try:
        con = sqlite3.connect('botcontent.db',  check_same_thread=False)
        return con
    except Error:
        print(Error)

def create_table(con):
    cursorObj = con.cursor()
    cursorObj.execute("CREATE TABLE IF NOT EXISTS content(id integer PRIMARY KEY, category text, name text)")
    con.commit()

def insert_in_db(con, dbdata):
    cursorObj = con.cursor()
    cursorObj.execute('''INSERT INTO content(category, name) VALUES(?, ?)''', dbdata)
    #cursorObj.execute("INSERT INTO content VALUES(2, 'фильм', 'Матрица')")
    con.commit()

def get_all_data(con):
    cursorObj = con.cursor()
    cursorObj.execute('SELECT * FROM content')
    rows = cursorObj.fetchall()
    for row in rows:
        print (row)
    return rows

