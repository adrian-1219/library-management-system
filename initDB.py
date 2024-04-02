# This file imports book data from Books.csv to sqlite3 database, adds a random generated number between 0 and 15 as each book's 
# availability and creates all other necessary tables. This only needs to be ran once (if library.db doesn't already exist)
# Books.csv taken from https://www.kaggle.com/datasets/arashnic/book-recommendation-dataset as suggested by professor

import sqlite3
import csv
from random import randrange
import datetime

connection = sqlite3.connect("library.db")
cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS books (ISBN TEXT PRIMARY KEY, title TEXT, author TEXT, yearPublished INTEGER, publisher TEXT, availability INTEGER)")

with open('book_info/Books.csv', mode ='r')as file:
    csvFile = csv.reader(file)
    for row in csvFile:
        if row[0] != "ISBN":
            cursor.execute("INSERT INTO books (ISBN, title, author, yearPublished, publisher, availability) \
                            VALUES (? ,? ,? ,? ,?, ?)", (row[0], row[1], row[2], row[3], row[4], randrange(16)))

cursor.execute('''CREATE TABLE IF NOT EXISTS account
                     (username TEXT PRIMARY KEY NOT NULL,
                      password TEXT NOT NULL)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS borrow
               (username TEXT NOT NULL,
               bookISBN TEXT NOT NULL,
               dateBorrowed TEXT NOT NULL,
               dateReturned TEXT,
               PRIMARY KEY (username, bookISBN, dateBorrowed))''')


connection.commit()
connection.close()