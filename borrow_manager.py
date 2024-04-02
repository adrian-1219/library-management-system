import sqlite3
import datetime
import book_manager

connection = sqlite3.connect("library.db")
cursor = connection.cursor()

class Borrow:
    def __init__(self, username, bookISBN, bookTitle, bookAuthor, dateBorrowed, dateReturned):
        self.username = username
        self.bookISBN = bookISBN
        self.bookTitle = bookTitle
        self.bookAuthor = bookAuthor
        self.dateBorrowed = dateBorrowed
        self.dateReturned = dateReturned

def getBorrowHistory(username, page = 1):
    resultsPerPage = 20
    cursor.execute("SELECT * FROM borrow as a JOIN books as b WHERE a.username = ? AND a.bookISBN = b.ISBN ORDER BY dateBorrowed DESC LIMIT ? OFFSET ?", (username, resultsPerPage, (page - 1) * resultsPerPage))
    result = cursor.fetchall()
    borrowResults = []
    for row in result:
        print(row)
        datetimeBorrowed = datetime.datetime.strptime(row[2].split(".", 1)[0], '%Y-%m-%d %H:%M:%S')
        datetimeReturned = None
        if row[3]:
            datetimeReturned = datetime.datetime.strptime(row[3].split(".", 1)[0], '%Y-%m-%d %H:%M:%S')
        borrowResults.append(Borrow(row[0], row[1], row[5], row[6], datetimeBorrowed, datetimeReturned))
    return borrowResults

def borrowed(username, bookISBN):
    # checks if user has already borrowed this book but have not returned it yet
    cursor.execute('''SELECT * FROM borrow WHERE username = ? AND bookISBN = ? AND dateReturned IS NULL''', (username, bookISBN))
    result = cursor.fetchall()
    return result

def borrowBook(username, bookISBN):
    book = book_manager.getBookDetails(bookISBN)
    if book.availability > 0 and not borrowed(username, bookISBN): 
        cursor.execute('''INSERT INTO borrow (username, bookISBN, dateBorrowed) VALUES (?, ?, ?)''', (username, bookISBN, datetime.datetime.now()))
        cursor.execute('''UPDATE books SET availability = ? WHERE ISBN = ?''', (book.availability - 1, bookISBN))
        connection.commit()

def returnBook(username, bookISBN):
    book = book_manager.getBookDetails(bookISBN)
    cursor.execute('''UPDATE borrow SET dateReturned = ? WHERE username = ? AND bookISBN = ? AND dateReturned IS NULL''', (datetime.datetime.now(), username, bookISBN))
    cursor.execute('''UPDATE books SET availability = ? WHERE ISBN = ?''', (book.availability + 1, bookISBN))
    connection.commit()


# testing
# returnBook("a", "0679425608")
print(getBorrowHistory("a", 1))
# borrowBook("a", "0679425608")
# print(getBorrowHistory("a")[0].dateReturned, getBorrowHistory("a")[0].dateBorrowed)