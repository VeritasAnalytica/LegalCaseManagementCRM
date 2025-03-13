from flask import g
import sqlite3 

def connect_to_database():
    #sql = sqlite3.connect('C:/Users/Leverify/Desktop/dashmin-1.0.0/books.db')
    sql = sqlite3.connect('/var/www/html/crm/books.db')
    sql.row_factory = sqlite3.Row
    return sql 


def get_database():
    if not hasattr(g, 'books_db'):
        g.books_db = connect_to_database()
    return g.books_db