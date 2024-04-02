# This file includes all classes and functions for the backend

import sqlite3

connection = sqlite3.connect("library.db")
cursor = connection.cursor()

class Book:
    def __init__(self, ISBN, title, author, yearPublished, publisher, availability):
        self.ISBN = ISBN
        self.title = title
        self.author = author
        self.yearPublished = yearPublished
        self.publisher = publisher
        self.availability = availability

def getBookDetails(id):
    cursor.execute("SELECT * FROM books WHERE ISBN = ?", (id,))
    result = cursor.fetchone()
    if not result:
        return None
    return toBook(result)

def toBook(sqlResult):
    return Book(sqlResult[0], sqlResult[1], sqlResult[2], sqlResult[3], sqlResult[4], sqlResult[5])

def toTuple(book):
    return (book.ISBN, book.title, book.author, book.yearPublished, book.publisher)

def search(keyword = None, yearRange = None, page = 1):
    resultsPerPage = 20
    if keyword and not yearRange:
        keyword = "%" + keyword + "%"
        cursor.execute("SELECT * FROM books WHERE ISBN LIKE ? OR title LIKE ? OR author LIKE ? OR publisher LIKE ? LIMIT ? OFFSET ?", (keyword, keyword, keyword, keyword, resultsPerPage, (page - 1) * resultsPerPage))
    elif keyword and yearRange:
        keyword = "%" + keyword + "%"
        if str(yearRange[0]) != "Any" and str(yearRange[1]) != "Any":
            cursor.execute("SELECT * FROM books WHERE yearPublished >= ? AND yearPublished <= ? AND (ISBN LIKE ? OR title LIKE ? OR author LIKE ? OR publisher LIKE ?) LIMIT ? OFFSET ?", \
                           (yearRange[0], yearRange[1], keyword, keyword, keyword, keyword, resultsPerPage, (page - 1) * resultsPerPage))
        elif str(yearRange[0]) != "Any":
            cursor.execute("SELECT * FROM books WHERE yearPublished >= ? AND (ISBN LIKE ? OR title LIKE ? OR author LIKE ? OR publisher LIKE ?) LIMIT ? OFFSET ?", \
                           (yearRange[0], keyword, keyword, keyword, keyword, resultsPerPage, (page - 1) * resultsPerPage))
        elif str(yearRange[1]) != "Any":
            cursor.execute("SELECT * FROM books WHERE yearPublished <= ? AND (ISBN LIKE ? OR title LIKE ? OR author LIKE ? OR publisher LIKE ?) LIMIT ? OFFSET ?", \
                           (yearRange[1], keyword, keyword, keyword, keyword, resultsPerPage, (page - 1) * resultsPerPage))
    elif not keyword and not yearRange:
        cursor.execute("SELECT * FROM books LIMIT ? OFFSET ?", (resultsPerPage, (page - 1) * resultsPerPage))
    else:
        if str(yearRange[0]) != "Any" and str(yearRange[1]) != "Any":
            cursor.execute("SELECT * FROM books WHERE yearPublished >= ? AND yearPublished <= ? LIMIT ? OFFSET ?", \
                           (yearRange[0], yearRange[1], resultsPerPage, (page - 1) * resultsPerPage))
        elif str(yearRange[0]) != "Any":
            cursor.execute("SELECT * FROM books WHERE yearPublished >= ? LIMIT ? OFFSET ?", \
                           (yearRange[0], resultsPerPage, (page - 1) * resultsPerPage))
        elif str(yearRange[1]) != "Any":
            cursor.execute("SELECT * FROM books WHERE yearPublished <= ? LIMIT ? OFFSET ?", \
                           (yearRange[1], resultsPerPage, (page - 1) * resultsPerPage))
    result = cursor.fetchmany(20) # Limits results to 20 per page
    bookSearchResults = []
    for row in result:
        print(row)
        bookSearchResults.append(toBook(row))
    return bookSearchResults
