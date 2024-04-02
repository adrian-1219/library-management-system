from tkinter import *
from tkinter import ttk
import book_manager

root = Tk()
root.title('Book Details')
# root.geometry('300x200')

# get book details from database given book id
pageResults = []

search_var = StringVar()

def search():
    global pageResults
    keyword = search_var.get()
    pageResults = models.search(keyword)
    displayResults(pageResults)

def displayResults(pageResults):
    treeview.delete(*treeview.get_children())
    for result in pageResults:
        treeview.insert(
            "",
            END,
            text=result.ISBN,
            values=(result.title, result.author, result.yearPublished, result.publisher)
        )

searchEntry = Entry(root, textvariable=search_var)
searchEntry.pack()

# test displaying with tkinter
# display one book
# label1 = Label(root, text="Title: " + book.title)
# label1.pack()
# label2 = Label(root, text="Author: " + book.author)
# label2.pack()
# label3 = Label(root, text="Year Published: " + str(book.yearPublished))
# label3.pack()
# label4 = Label(root, text="Publisher: " + book.publisher)
# label4.pack()
# label5 = Label(root, text="ISBN: " + book.ISBN)
# label5.pack()

# display search results
searchBtn=Button(root,text = 'Search', command = search)
searchBtn.pack()

treeview = ttk.Treeview(columns=("title", "author", "year", "publisher"))
treeview.heading("#0", text="ISBN")
treeview.heading("title", text="Title")
treeview.heading("author", text="Author")
treeview.heading("year", text="Year")
treeview.heading("publisher", text="Publisher")
treeview.pack()


root.mainloop()

