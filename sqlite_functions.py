import sqlite3
from sqlite3 import Error

def db_connection():
    try:
        con = sqlite3.connect('botcontent.db')
        return con
    except Error:
        print(Error)

def create_table(con):
    cursorObj = con.cursor()
    cursorObj.execute("CREATE TABLE IF NOT EXISTS content(id integer PRIMARY KEY, category text, name text)")
    con.commit()

con = db_connection()
create_table(con)

def insert_in_db(con):
    cursorObj = con.cursor()
    cursorObj.execute("INSERT INTO content VALUES(1, 'книга', 'Война и Мир')")
    cursorObj.execute("INSERT INTO content VALUES(2, 'фильм', 'Матрица')")
    con.commit()

insert_in_db(con)

def get_all_data(con):
    cursorObj = con.cursor()
    cursorObj.execute('SELECT * FROM content')
    rows = cursorObj.fetchall()
    for row in rows:
        print(row)

get_all_data(con)