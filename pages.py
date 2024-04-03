import random
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from PIL import Image, ImageTk
from tkinter.font import Font


import requests

from account_manager import RegisterFunction
import book_manager, datetime, borrow_manager


class StartPage(tk.Frame):
    """This is the start page of the library management system. It will allow the user to register or login.
    background image from: https://www.google.ca/imgres?imgurl=https://c4.wallpaperflare.com/wallpaper/479/101/113/germany-saxony-gorlitz-hall-historical-literature-wallpaper-preview.jpg&tbnid=ZhqeeBVaHxzzJM&vet=1&imgrefurl=https://www.wallpaperflare.com/search?wallpaper%3Dlibrary&docid=Uu-4mrzVh9DQcM&w=728&h=410"""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        canvas = tk.Canvas(self, width=1280, height=680, highlightthickness=0)
        canvas.pack(fill='both', expand=True)
        
        # background image
        self.start_image = Image.open("assets/start.png")
        self.resized_start_image = self.start_image.resize((1280, 680), Image.Resampling.LANCZOS)
        self.start_background = ImageTk.PhotoImage(self.resized_start_image)
        canvas.create_image(640, 340, image=self.start_background)

        # draw text
        canvas.create_text(640, 200, text="Library Management System", font="Helvetica 30 bold", fill="white")

        style = ttk.Style()

        # change to 'aqua' for originally sytled buttons
        style.theme_use('alt')
        style.configure('Transparent.TButton', borderwidth=0, padding=0)

        ttk.Button(self, text="Register", style='Transparent.TButton', command=lambda: controller.show_frame("RegisterPage")).place(relx=0.5, rely=0.4, anchor="center")
        ttk.Button(self, text="Login", style='Transparent.TButton', command=lambda: controller.show_frame("LoginPage")).place(relx=0.5, rely=0.5, anchor="center")



class RegisterPage(tk.Frame):
    """This is the register page of the library management system. It will allow the user to register to the system.
    background image from: https://blog.theadl.com/2018/07/06/digital-libraries-from-keepers-to-communicators/"""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        # tk.Label(self, text="Register").place(relx=0.5, rely=0.2, anchor="center")

        canvas = tk.Canvas(self, width=1280, height=680, highlightthickness=0)
        canvas.pack(fill='both', expand=True)
        
        # background 
        self.register_image = Image.open("assets/login-register.png")
        self.resized_register_image = self.register_image.resize((1280, 680), Image.Resampling.LANCZOS)
        self.register_background = ImageTk.PhotoImage(self.resized_register_image)
        canvas.create_image(640, 340, image=self.register_background)
        # draw text
        canvas.create_text(640, 200, text="Register", font="Helvetica 30 bold", fill="white")
        # configure style 
        style = ttk.Style()
        # change to 'aqua' for originally sytled buttons
        style.theme_use('alt')
        style.configure('Transparent.TButton', borderwidth=0, padding=0)

        # a button to go back to the start page on the top left corner
        ttk.Button(self, text="Back", style='Transparent.TButton', command=lambda: controller.show_frame("StartPage")).place(relx=0.1, rely=0.1, anchor="center")


        # entry boxes for the username, password, and verify password
        username_label = tk.Label(self, text="Username")
        username_label.place(relx=0.45, rely=0.4, anchor="e")
        self.username_entry = ttk.Entry(self)
        self.username_entry.place(relx=0.45, rely=0.4, anchor="w")

        password_label = tk.Label(self, text="Password")
        password_label.place(relx=0.45, rely=0.5, anchor="e")
        # show the password as asterisks
        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.place(relx=0.45, rely=0.5, anchor="w")

        verify_password_label = tk.Label(self, text="Verify Password")
        verify_password_label.place(relx=0.45, rely=0.6, anchor="e")
        self.verify_password_entry = ttk.Entry(self, show="*")
        self.verify_password_entry.place(relx=0.45, rely=0.6, anchor="w")

        ttk.Button(self, text="Submit", style='Transparent.TButton',
                   command=self.register).place(relx=0.5, rely=0.7, anchor="center")

    def register(self):
        """this function will register the user into the database and check if the username already exists or not
        background image from: https://blog.theadl.com/2018/07/06/digital-libraries-from-keepers-to-communicators/"""
        username = self.username_entry.get()
        password = self.password_entry.get()
        v_password = self.verify_password_entry.get()

        if username == '' or password == '':
            # if the username or password is empty, it will show an error message
            messagebox.showinfo('Error', 'Please enter username and password')
        elif password != v_password:
            # if the password and verify password is not the same, it will show an error message
            messagebox.showinfo('Error', 'Please check the password')
        else:
            # if the username is already in the database, it will show an error message
            result = RegisterFunction.check_username(username)
            if result:
                messagebox.showinfo('Error', 'Username already exists')
            else:
                # if the username is not in the database, it will register the user into the database
                RegisterFunction.insert_account(username, password)
                messagebox.showinfo('Success', 'Account registered successfully')
                # it will clear the entry boxes
                self.username_entry.delete(0, tk.END)
                self.password_entry.delete(0, tk.END)
                self.controller.show_frame("HomePage")


class LoginPage(tk.Frame):
    """This is the login page of the library management system. It will allow the user to login to the system."""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        controller.add_menu(self)

        canvas = tk.Canvas(self, width=1280, height=680, highlightthickness=0)
        canvas.pack(fill='both', expand=True)
        
        # background 
        self.login_image = Image.open("assets/login-register.png")
        self.resized_login_image = self.login_image.resize((1280, 680), Image.Resampling.LANCZOS)
        self.login_background = ImageTk.PhotoImage(self.resized_login_image)
        canvas.create_image(640, 340, image=self.login_background)
        # draw text
        canvas.create_text(640, 200, text="Login", font="Helvetica 30 bold", fill="white")
        # configure style 
        style = ttk.Style()
        # change to 'aqua' for originally sytled buttons
        style.theme_use('alt')
        style.configure('Transparent.TButton', borderwidth=0, padding=0)



        # tk.Label(self, text="Login").place(relx=0.5, rely=0.3, anchor="center")

        # a button to go back to the start page on the top left corner
        ttk.Button(self, text="Back", style='Transparent.TButton', command=lambda: controller.show_frame("StartPage")).place(relx=0.1, rely=0.1, anchor="center")

        username_label = tk.Label(self, text="Username: ")
        username_label.place(relx=0.45, rely=0.4, anchor="e")
        self.username_entry = ttk.Entry(self)
        self.username_entry.place(relx=0.45, rely=0.4, anchor="w")

        password_label = tk.Label(self, text="Password: ")
        password_label.place(relx=0.45, rely=0.5, anchor="e")
        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.place(relx=0.45, rely=0.5, anchor="w")

        ttk.Button(self, text="Login", style='Transparent.TButton', 
                   command=self.attempt_login).place(relx=0.5, rely=0.6, anchor="center")

    def attempt_login(self):
        """this function will check if the username and password is correct or not"""
        # get the current username and password
        username = self.username_entry.get()
        password = self.password_entry.get()
        # call the check_password function
        if self.check_password(username, password):
            messagebox.showinfo("Login Successful", "You have successfully logged in.")
            self.controller.show_frame("HomePage")
            self.controller.username = username
        else:
            messagebox.showerror("Login Failed", "Incorrect username or password.")

    def check_password(self, username, password):
        # check if the username is in the database
        result = RegisterFunction.check_username(username)
        # if the username is in the database, it will check if the password is correct or not
        if result and result[1] == password:
            self.controller.current_account = username
            return True
        return False

    def logout(self):
        # this function will log out the user and return to the start page
        # set the current account to None
        self.controller.current_account = None
        messagebox.showinfo("Logout Successful", "You have been logged out.")
        self.controller.show_frame("StartPage")


class HomePage(tk.Frame):
    """This is the home page of the library management system. It will display the books of the day and the toolbar."""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # put the toolbar on the top of the page
        self.toolbar = CustomToolbar(self, controller)
        self.toolbar.pack(side="top", fill="x")

        # a frame to display the books
        self.books_frame = tk.Frame(self)
        self.books_frame.pack(expand=True, fill="both", padx=20, pady=20)

        self.display_books()
        
    def display_books(self):
        # get all the books from the database
        # all_books = book_manager.search()
        # random_books = random.sample(all_books, min(len(all_books), 10))

        # get random books from the database by choosing a random page and a random entry
        random_books = book_manager.fetch_random_books(10)
        tk.Label(self.books_frame, text="   Books of The Day", font=("Helvetica", 20, "bold"), anchor="w").pack(fill="x", pady=(10, 20))

        for book in random_books:
            book_btn = ttk.Button(self.books_frame, text=f"•  {book.title} by {book.author} ({book.yearPublished})",
                                  style='Link.TButton',
                                  command=lambda b=book: self.show_book_info(b))
            book_btn.pack(fill='x', padx=20, pady=5)

    def show_book_info(self, book):
        # invoke the show_book function in the controller to tkraise the BookDetailsPage
        self.controller.show_book("BookDetailsPage", book)


class BookDetailsPage(tk.Frame):
    """This page will display the details of a book. It will show the title,
    author, year published, publisher, and ISBN. Allowing the user to borrow or return the book in this page"""
    def __init__(self, parent, controller, book):
        super().__init__(parent)
        self.controller = controller
        self.book = book

        self.toolbar = CustomToolbar(self, controller)
        self.toolbar.pack(side="top", fill="x")
        tk.Label(self, text="Book Details", font=("Helvetica", 20, "bold")).pack(pady=10)

        # Display book information
        self.displayBookDetails()

        # check the current username logged in and try to display in the top left corner for later use
        print(self.controller.username)

        # Borrow or return button
        # ------------------this need to be updated (maybe only show the return button if its
        # borrowed instead of replacing it?-------------------------------------------
        if borrow_manager.borrowed(self.controller.username, self.book.ISBN):
            self.borrowReturnBtn = tk.Button(self, text="Return", command=self.returnBook)
            self.borrowReturnBtn.pack()
        else:
            self.borrowReturnBtn = tk.Button(self, text="Borrow", command=self.borrowBook)
            self.borrowReturnBtn.pack()

    def displayBookDetails(self):
        """Display book details on the page"""
        # get the summary and rating of the book from the google books api
        summary_rating = self.get_book_details(str(self.book.ISBN))
        summary, rating = summary_rating

        # details container frame
        details_frame = tk.Frame(self)
        details_frame.pack(fill='x', padx=10, pady=10)

        regular_font = ("Helvetica", 16)
        # make the bold_font bold and blue color
        bold_font = ("Helvetica", 16, "bold")
        text_color = "#68fcf7"

        # Title
        tk.Label(details_frame, text="Title: ", font=regular_font).pack(anchor='w')
        self.titleLabel = tk.Label(details_frame, text=f"{self.book.title}", font=bold_font, fg=text_color)
        self.titleLabel.pack(anchor='w')

        # Author
        tk.Label(details_frame, text="Author: ", font=regular_font).pack(anchor='w')
        self.authorLabel = tk.Label(details_frame, text=f"{self.book.author}", font=bold_font, fg=text_color)
        self.authorLabel.pack(anchor='w')

        # ISBN
        tk.Label(details_frame, text="ISBN: ", font=regular_font).pack(anchor='w')
        self.ISBNLabel = tk.Label(details_frame, text=f"{self.book.ISBN}", font=bold_font, fg=text_color)
        self.ISBNLabel.pack(anchor='w')

        # Year Published
        tk.Label(details_frame, text="Year Published: ", font=regular_font).pack(anchor='w')
        self.yearLabel = tk.Label(details_frame, text=f"{self.book.yearPublished}", font=bold_font, fg=text_color)
        self.yearLabel.pack(anchor='w')

        # Publisher
        tk.Label(details_frame, text="Publisher: ", font=regular_font).pack(anchor='w')
        self.publisherLabel = tk.Label(details_frame, text=f"{self.book.publisher}", font=bold_font, fg=text_color)
        self.publisherLabel.pack(anchor='w')

        # Rating
        tk.Label(details_frame, text="Rating: ", font=regular_font).pack(anchor='w')
        self.ratingLabel = tk.Label(details_frame, text=f"{rating}", font=bold_font, fg=text_color)
        self.ratingLabel.pack(anchor='w')

        # Only display 1000 characters of the summary
        formatted_summary = summary[:1000] + "..." if len(summary) > 1000 else summary
        # only display 180 characters of the formatted summary each line
        formatted_summary = "\n".join([formatted_summary[i:i+180] for i in range(0, len(formatted_summary), 180)])

        tk.Label(details_frame, text="Summary: ", font=regular_font).pack(anchor='w')
        self.summaryLabel = tk.Label(details_frame, text=f"{formatted_summary}", font=("Helvetica", 16), justify='left', fg=text_color)
        self.summaryLabel.pack(anchor='w')

        self.availabilityLabel = tk.Label(details_frame, text=f"Availability: {self.book.availability}", font=("Helvetica", 16))
        self.availabilityLabel.pack(anchor='e', pady=15, padx=15)

    def clearBookDetails(self):
        """Clear book details from the page"""
        self.titleLabel.pack_forget()
        self.authorLabel.pack_forget()
        self.ISBNLabel.pack_forget()
        self.yearLabel.pack_forget()
        self.publisherLabel.pack_forget()
        self.availabilityLabel.pack_forget()

    def returnBook(self):
        """Return the book and update the page"""
        borrow_manager.returnBook(self.controller.username, self.book.ISBN)
        # refresh details
        self.book = book_manager.getBookDetails(self.book.ISBN)
        self.clearBookDetails()
        self.displayBookDetails()
        # change button (or maybe just hide the button if it's returned?, or show a message that it's returned)
        self.borrowReturnBtn.pack_forget()
        self.borrowReturnBtn = tk.Button(self, text="Borrow", command=self.borrowBook)
        self.borrowReturnBtn.pack()

    def borrowBook(self):
        borrow_manager.borrowBook(self.controller.username, self.book.ISBN)
        # refresh details
        self.book = book_manager.getBookDetails(self.book.ISBN)
        self.clearBookDetails()
        self.displayBookDetails()
        # change button
        self.borrowReturnBtn.pack_forget()
        self.borrowReturnBtn = tk.Button(self, text="Return", command=self.returnBook)
        self.borrowReturnBtn.pack()

    # this function utilizes googlebooks api to get the book details
    def get_book_details(self, isbn: str) -> (str, int):
        # credit to https://www.datacamp.com/tutorial/making-http-requests-in-python
        # get the book details from the google books api
        url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"
        response = requests.get(url)
        # notes: status code of 200 means server successfully processed
        if response.status_code == 200:
            data = response.json()
            # if "totalItems" is greater than 0, means the book is found
            if data["totalItems"] > 0:
                book_info = data["items"][0]["volumeInfo"]
                summary = book_info.get("description", "No summary available")
                rating = book_info.get("averageRating", "No rating available")
                return (summary, rating)
            else:
                return "No results found"
        else:
            return "Failed to fetch data"



class SearchPage(tk.Frame):
    """This page will allow the user to search for books by title, author, year, or publisher."""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.pageResults = []
        self.page = 1
        self.pageVar = tk.StringVar()
        self.pageVar.set(str(self.page))

        self.toolbar = CustomToolbar(self, controller)
        self.toolbar.pack(side="top", fill="x")

        # Container Frame for search
        search_container = tk.Frame(self)
        search_container.pack(side="top", fill="x", padx=10, pady=10)

        # Year range selection for search
        # print(datetime.date.today())
        years = list(range(1900, datetime.date.today().year + 1))
        years.append("Any")
        self.yearRangeLabel = tk.Label(search_container, text="Year Range: ")
        self.yearRangeLabel.pack(side="left")
        self.yearStartCombobox = ttk.Combobox(search_container, values=years, width=5)
        self.yearStartCombobox.pack(side="left")
        self.yearStartCombobox.set("Any")
        self.yearEndCombobox = ttk.Combobox(search_container, values=years, width=5)
        self.yearEndCombobox.pack(side="left")
        self.yearEndCombobox.set("Any")
        
        # Search Entry
        self.searchLabel = tk.Label(search_container, text=" Search: ")
        self.searchLabel.pack(side="left")
        self.search_var = tk.StringVar()
        self.searchEntry = tk.Entry(search_container, textvariable=self.search_var)
        self.searchEntry.pack(side="left", expand=True, fill="x", padx=(0, 5))

        # Search Button
        searchBtn = tk.Button(search_container, text='Search', command=self.newSearch)
        searchBtn.pack(side="left")

        # Search results treeview
        self.treeview = ttk.Treeview(self, columns=("title", "author", "year", "publisher"))
        self.treeview.column("#0", width=100)
        self.treeview.column("title", width=600)
        self.treeview.column("author", width=200)
        self.treeview.column("year", width=50)
        self.treeview.heading("#0", text="ISBN")
        self.treeview.heading("title", text="Title")
        self.treeview.heading("author", text="Author")
        self.treeview.heading("year", text="Year")
        self.treeview.heading("publisher", text="Publisher")
        self.treeview.pack(side="top", expand=True, fill="both", padx=10, pady=(5, 0))

        # Result page controls
        pageContainer = tk.Frame(self)
        pageContainer.pack(side="top", fill="x", pady=5)
        self.prevPageBtn = tk.Button(pageContainer, text="<<<", command=self.prevPage, state="disabled")
        self.prevPageBtn.pack(side="left")
        self.pageNum = tk.Label(pageContainer, textvariable=self.pageVar, width=5)
        self.pageNum.pack(side="left")
        self.nextPageBtn = tk.Button(pageContainer, text=">>>", command=self.nextPage, state="disabled")
        self.nextPageBtn.pack(side="left")
        self.paddingRight = tk.Label(pageContainer)
        self.paddingRight.pack(side="left", fill="x", expand=True)
        self.detailsBtn = tk.Button(pageContainer, text="Details", command=self.goToBookDetails)
        self.detailsBtn.pack(side="left")



    def newSearch(self):
        """Reset page and search for books based on the search"""
        self.page = 1 
        self.pageVar.set(str(self.page))
        self.search()

    def search(self):
        """Search for books based on the search criteria and display the results."""
        keyword = self.search_var.get()
        yearStart = self.yearStartCombobox.get()
        yearEnd = self.yearEndCombobox.get()
        yearRange = [yearStart, yearEnd]
        if str(yearStart) == "Any" and str(yearEnd) == "Any":
            yearRange = None
        self.pageResults = book_manager.search(keyword, yearRange, self.page)
        self.displayResults()

        # Set page controls
        if self.page == 1:
            self.prevPageBtn["state"] = "disabled"
        else:
            self.prevPageBtn["state"] = "normal"
        if book_manager.search(keyword, yearRange, self.page + 1):
            self.nextPageBtn["state"] = "normal"
        else:
            self.nextPageBtn["state"] = "disabled"

    def nextPage(self):
        self.page += 1 
        self.pageVar.set(str(self.page))
        self.search()

    def prevPage(self):
        self.page -= 1 
        self.pageVar.set(str(self.page))
        self.search()

    def displayResults(self):
        """Display search results in the treeview."""
        self.treeview.delete(*self.treeview.get_children())
        for result in self.pageResults:
            self.treeview.insert(
                "",
                tk.END,
                text=result.ISBN,
                values=(result.title, result.author, result.yearPublished, result.publisher)
            )
    
    def goToBookDetails(self):
        curItem = self.treeview.item(self.treeview.focus())
        # print("focus(): ", self.treeview.focus())
        # print(curItem)
        if curItem["text"]:
            book = book_manager.getBookDetails(curItem["text"])
            self.controller.show_book("BookDetailsPage", book)


class BorrowedBooksPage(tk.Frame):
    """This page will display the books that the user has borrowed. It will show the title,
    author, date borrowed, and status."""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.toolbar = CustomToolbar(self, controller)
        self.toolbar.pack(side="top", fill="x")

        self.loanPeriod = 21 # Set book loan period to 21 days

        tk.Label(self, text="Books Borrowed History", font=("Helvetica", 20, "bold")).pack(pady=10)
        self.page = 1
        self.pageVar = tk.StringVar()
        self.pageVar.set(str(self.page))

        # Borrow history treeview
        self.treeview = ttk.Treeview(self, columns=("title", "author", "dateBorrowed", "status"))
        self.treeview.column("#0", width=100)
        self.treeview.column("title", width=600)
        self.treeview.column("author", width=200)
        self.treeview.column("dateBorrowed", width=200)
        self.treeview.column("status")
        self.treeview.heading("#0", text="ISBN")
        self.treeview.heading("title", text="Title")
        self.treeview.heading("author", text="Author")
        self.treeview.heading("dateBorrowed", text="Date Borrowed")
        self.treeview.heading("status", text="Status")
        self.treeview.pack(side="top", expand=True, fill="both", padx=10, pady=(5, 0))

        # Borrow history page controls
        pageContainer = tk.Frame(self)
        pageContainer.pack(side="top", fill="x", pady=5)
        self.prevPageBtn = tk.Button(pageContainer, text="<<<", command=self.prevPage, state="disabled")
        self.prevPageBtn.pack(side="left")
        self.pageNum = tk.Label(pageContainer, textvariable=self.pageVar, width=5)
        self.pageNum.pack(side="left")
        self.nextPageBtn = tk.Button(pageContainer, text=">>>", command=self.nextPage, state="disabled")
        self.nextPageBtn.pack(side="left")
        self.paddingRight = tk.Label(pageContainer)
        self.paddingRight.pack(side="left", fill="x", expand=True)
        self.detailsBtn = tk.Button(pageContainer, text="Details", command=self.goToBookDetails)
        self.detailsBtn.pack(side="left")

        self.pageResults = borrow_manager.getBorrowHistory(self.controller.username, self.page)
        # print(self.controller.username, self.page)
        # print(self.pageResults)
        self.displayResults()

    def nextPage(self):
        self.page += 1 
        self.pageVar.set(str(self.page))
        self.pageResults = borrow_manager.getBorrowHistory(self.controller.username, self.page)
        self.displayResults()

    def prevPage(self):
        self.page -= 1 
        self.pageVar.set(str(self.page))
        self.pageResults = borrow_manager.getBorrowHistory(self.controller.username, self.page)
        self.displayResults()

    def displayResults(self):
        self.treeview.delete(*self.treeview.get_children())
        for result in self.pageResults:
            status = ""
            returnDate = result.dateBorrowed + datetime.timedelta(days=self.loanPeriod)
            if not result.dateReturned:
                # check how long its been since date borrowed
                if datetime.datetime.now() > returnDate:
                    status = "OVERDUE"
                else:
                    status = "DUE ON " + returnDate.strftime("%Y-%m-%d %H:%M:%S")
            else:
                if result.dateReturned > returnDate:
                    status = "RETURNED LATE"
                else:
                    status = "RETURNED"
            self.treeview.insert(
                "",
                tk.END,
                text=result.bookISBN,
                values=(result.bookTitle, result.bookAuthor, result.dateBorrowed, status)
            )
        # Set page controls
        if self.page == 1:
            self.prevPageBtn["state"] = "disabled"
        else:
            self.prevPageBtn["state"] = "normal"
        if borrow_manager.getBorrowHistory(self.controller.username, self.page + 1):
            self.nextPageBtn["state"] = "normal"
        else:
            self.nextPageBtn["state"] = "disabled"

    def goToBookDetails(self):
        curItem = self.treeview.item(self.treeview.focus())
        # print("focus(): ", self.treeview.focus())
        # print(curItem)
        if curItem["text"]:
            book = book_manager.getBookDetails(curItem["text"])
            self.controller.show_book("BookDetailsPage", book)


class AccountPage(tk.Frame):
    # wait for account_manager.py to be implemented first
    # second option: update the account info in this class

    # Placeholder for AccountPage and Borrowed books details go in this page
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.toolbar = CustomToolbar(self, controller)
        self.toolbar.pack(side="top", fill="x")
        # self.username = None
    
        tk.Label(self, text="Account Page", font=("Helvetica", 20)).place(relx=0.5, rely=0.1, anchor="center")
        tk.Label(self, text="Username:").place(relx=0.3, rely=0.3, anchor="e")
        # tk.Label(self, text=self.username).place(relx=0.35, rely=0.3, anchor="w")
    
        tk.Label(self, text="Password:").place(relx=0.3, rely=0.4, anchor="e")
        # password = self.get_password(self.username)
        # tk.Label(self, text=password).place(relx=0.35, rely=0.4, anchor="w")
    
        ttk.Button(self, text="Modify Username", command=self.modify_username).place(relx=0.5, rely=0.5,
                                                                                     anchor="center")
        ttk.Button(self, text="Modify Password", command=self.modify_password).place(relx=0.5, rely=0.6,
                                                                                     anchor="center")
        ttk.Button(self, text="Modify Email", command=self.modify_email).place(relx=0.5, rely=0.7,
                                                                               anchor="center")
        ttk.Button(self, text="Logout", command=self.logout).place(relx=0.5, rely=0.8, anchor="center")


    
    # def set_username(self, username):
    #     self.username = username

    def get_password(self, username):
        conn = sqlite3.connect('account.db')
        c = conn.cursor()
        c.execute("SELECT password FROM account WHERE username = ?", (username,))
        result = c.fetchone()
        conn.close()
        return result[0] if result else ""
        pass
    
    def modify_username(self):
        new_username = simpledialog.askstring("Input", "Enter new username:", parent=self)
        if new_username:
            result = RegisterFunction.check_username(new_username)
            if result:
                messagebox.showinfo('Error', 'Username already exists')
            else:
                conn = sqlite3.connect('account.db')
                c = conn.cursor()
                c.execute("UPDATE account SET username = ? WHERE username = ?", (new_username, self.username))
                conn.commit()
                conn.close()
                messagebox.showinfo('Success', 'Username modified successfully')
                self.controller.show_frame(AccountPage, new_username)
        pass
    
    def modify_password(self):
        new_password = simpledialog.askstring("Input", "Enter new password:", parent=self)
        if new_password:
            conn = sqlite3.connect('account.db')
            c = conn.cursor()
            c.execute("UPDATE account SET password = ? WHERE username = ?", (new_password, self.username))
            conn.commit()
            conn.close()
            messagebox.showinfo('Success', 'Password modified successfully')
        pass
    
    def modify_email(self):
        new_email = simpledialog.askstring("Input", "Enter new email:", parent=self)
        if new_email:
            conn = sqlite3.connect('account.db')
            c = conn.cursor()
            c.execute("UPDATE account SET email = ? WHERE username = ?", (new_email, self.username))
            conn.commit()
            conn.close()
            messagebox.showinfo('Success', 'Email modified successfully')
        pass
    
    def logout(self):
        RegisterFunction.delete_account(self.username)
        messagebox.showinfo('Success', 'Account deleted successfully')
        self.controller.show_frame(StartPage)


class RecommendPage(tk.Frame):
    # for books suggestions based on user's borrowing history
    pass


class CustomToolbar(tk.Frame):
    """This is a custom toolbar that will be displayed on the top of the page.
    It will have the home button, account menu,
    Search Button icon from: https://www.shareicon.net/loop-view-magnifier-zoom-search-eye-research-magnifying-glass-explore-magnifying-find-glass-82290"""
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        self.search_icon = tk.PhotoImage(file="assets/search.png")

        # home page button
        tk.Button(self, text="Home", command=lambda: controller.show_frame("HomePage")).pack(side="left", padx=10)

        # account menu
        account_menu = tk.Menubutton(self, text="Account", relief=tk.RAISED)
        account_menu.menu = tk.Menu(account_menu, tearoff=0)
        account_menu["menu"] = account_menu.menu
        account_menu.menu.add_command(label="Account Setting", command=lambda: controller.show_frame("AccountPage"))
        account_menu.menu.add_command(label="Borrowed Books", command=lambda: controller.show_borrow_history("BorrowedBooksPage"))
        account_menu.menu.add_command(label="Recommendation", command=lambda: controller.show_frame("RecommendPage"))
        account_menu.menu.add_command(label="Log out", command=lambda: controller.show_frame("StartPage"))
        account_menu.pack(side="right", padx=10)

        # Search Button 
        tk.Button(self, image=self.search_icon, command=lambda: controller.show_frame("SearchPage")).pack(side="right", padx=10)

        # Accessibility Menu
        accessibility_menu = tk.Menubutton(self, text="Accessibility", relief=tk.RAISED)
        accessibility_menu.menu = tk.Menu(accessibility_menu, tearoff=0)
        accessibility_menu["menu"] = accessibility_menu.menu
        accessibility_menu.pack(side="right", padx=10)

        # Font Menu
        font_menu = tk.Menu(accessibility_menu.menu, tearoff=0)
        font_menu.add_command(label="Size Up", command=self.fontsize_up)
        font_menu.add_command(label="Normal", command=self.reset_fontsize)
        font_menu.add_command(label="Size Down", command=self.fontsize_down)
        accessibility_menu.menu.add_cascade(label='Font', menu=font_menu, underline=0)

        # Colour menu
        accessibility_menu.menu.add_command(label="Colour", command=self.change_colour)
               

    def fontsize_up(self):
        new_font = Font(family='Times New Roman', size=30)

        # new font on tk.Label and tk.Button widgets
        for widget in self.controller.walk_widgets():
            if isinstance(widget, tk.Label) or isinstance(widget, tk.Button):
                widget.config(font=new_font)
            elif isinstance(widget, ttk.Entry) or isinstance(widget, tk.Text):
                widget['font'] = new_font

            # change style of ttk widgets
            elif isinstance(widget, (ttk.Button, ttk.Label)):
                style_name = 'TFont.TButton' if isinstance(widget, ttk.Button) else 'TFont.TLabel'
                style = ttk.Style()
                style.configure(style_name, font=new_font)
                widget.configure(style=style_name)
                style.configure('Treeview', font=new_font)
                style.configure('Treeview.Heading', font=new_font)

    def fontsize_down(self):
        new_font = Font(family='Times New Roman', size=9)

        # new font on tk.Label and tk.Button widgets
        for widget in self.controller.walk_widgets():
            if isinstance(widget, tk.Label) or isinstance(widget, tk.Button):
                widget.config(font=new_font)
            elif isinstance(widget, ttk.Entry) or isinstance(widget, tk.Text):
                widget['font'] = new_font

            # change style of ttk widgets
            elif isinstance(widget, (ttk.Button, ttk.Label)):
                style_name = 'TFont.TButton' if isinstance(widget, ttk.Button) else 'TFont.TLabel'
                style = ttk.Style()
                style.configure(style_name, font=new_font)
                widget.configure(style=style_name)
                style.configure('Treeview', font=new_font)
                style.configure('Treeview.Heading', font=new_font)

    def reset_fontsize(self):
        normal_font = Font(size=13)
        title_font = Font(size=20, weight='bold')
        style = ttk.Style()

        # styles for widgets
        style.configure('TLabel', font=title_font)
        style.configure('TButton', font=normal_font)


        for widget in self.controller.walk_widgets():
            if isinstance(widget, tk.Label):
                # title font for labels
                widget.config(font=title_font)
            elif isinstance(widget, (tk.Button, tk.Entry)):
                # normal font for buttons/entries
                widget.config(font=normal_font)
            elif isinstance(widget, ttk.Widget):
                # font for widget types
                wtype = widget.winfo_class()
                if 'Label' in wtype:
                    widget.config(style='TLabel')
                elif 'Button' in wtype:
                    widget.config(style='TButton')



    def change_colour(self):
        # for accessibility, change the colour of the text for better readability
        pass
