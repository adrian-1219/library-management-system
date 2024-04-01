# This file imports book data from Books.csv to sqlite3 database, this only needs to be ran once (if library.db doesn't already exist)
# Books.csv taken from https://www.kaggle.com/datasets/arashnic/book-recommendation-dataset as suggested by professor

import sqlite3
import csv

connection = sqlite3.connect("library.db")
cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS books (ISBN TEXT PRIMARY KEY, title TEXT, author TEXT, yearPublished INTEGER, publisher TEXT)")

with open('book_info/Books.csv', mode ='r')as file:
    csvFile = csv.reader(file)
    for row in csvFile:
        if row[0] != "ISBN":
            cursor.execute("INSERT INTO books (ISBN, title, author, yearPublished, publisher) \
                            VALUES (? ,? ,? ,? ,?)", (row[0], row[1], row[2], row[3], row[4]))

connection.commit()
connection.close()