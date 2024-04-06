import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from tkinter.font import Font
import requests
from PIL import Image, ImageTk
import account_manager
import book_manager
import borrow_manager
import datetime
from account_manager import RegisterFunction


class StartPage(tk.Frame):
    """This is the start page of the library management system. It will allow the user to register or login.
    background image from: https://upload.wikimedia.org/wikipedia/commons/5/5a/Books_HD_%288314929977%29.jpg"""

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        canvas = tk.Canvas(self, width=1380, height=680, highlightthickness=0)
        canvas.pack(fill='both', expand=True)

        # background image
        self.start_image = Image.open("assets/start.png")
        self.resized_start_image = self.start_image.resize((1280, 680))
        self.start_background = ImageTk.PhotoImage(self.resized_start_image)
        canvas.create_image(640, 340, image=self.start_background)

        # draw text
        canvas.create_text(640, 230, text="Library Management System", font="Georgia 45 bold", fill="#2196F3")

        style = ttk.Style()

        # change to 'aqua' for originally styled buttons
        style.theme_use('alt')
        style.configure('Transparent.TButton',
                        background='SystemButtonFace',
                        relief="flat",
                        foreground="black",
                        )

        ttk.Button(self, text="Register", style='Transparent.TButton',
                   command=lambda: controller.show_frame("RegisterPage")).place(relx=0.5, rely=0.5, anchor="center")
        ttk.Button(self, text="Login", style='Transparent.TButton',
                   command=lambda: controller.show_frame("LoginPage")).place(relx=0.5, rely=0.55, anchor="center")


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
        self.resized_register_image = self.register_image.resize((1280, 680))
        self.register_background = ImageTk.PhotoImage(self.resized_register_image)
        canvas.create_image(640, 340, image=self.register_background)
        # draw text
        canvas.create_text(640, 200, text="Register", font="Helvetica 30 bold", fill="#FFE082")
        # configure style
        style = ttk.Style()
        # change to 'aqua' for originally sytled buttons
        style.theme_use('alt')
        style.configure('Transparent.TButton', borderwidth=0, padding=0)

        # a button to go back to the start page on the top left corner
        ttk.Button(self, text="Back", style='Transparent.TButton',
                   command=lambda: controller.show_frame("StartPage")).place(relx=0.1, rely=0.1, anchor="center")

        canvas.create_text(515, 270, text="Username:", font="Helvetica 15", fill="#FFE082")
        canvas.create_text(515, 340, text="Password:", font="Helvetica 15", fill="#FFE082")
        canvas.create_text(510, 410, text="Verify Password:", font="Helvetica 15", fill="#FFE082")
        # entry boxes for the username, password, and verify password
        self.username_placeholder = "Bookworm123"
        self.username_entry = tk.Entry(self, bg="#E0E0E0", border=0, relief="sunken")
        self.username_entry.insert(0, self.username_placeholder)
        self.username_entry.bind('<FocusIn>',
                                 lambda event, e=self.username_entry: LoginPage.
                                 on_entry_click(e, self.username_placeholder))
        self.username_entry.bind('<FocusOut>',
                                 lambda event, e=self.username_entry: LoginPage.
                                 on_entry_click(e, self.username_placeholder))
        self.username_entry.configure(fg='grey')
        self.username_entry.place(relx=0.45, rely=0.4, anchor="w")

        # show the password as asterisks
        self.password_placeholder = "12345"
        self.password_entry = tk.Entry(self, show="*", bg="#E0E0E0", borderwidth=0, relief="sunken")
        self.password_entry.insert(0, self.password_placeholder)

        self.password_entry.bind('<FocusIn>', lambda event, e=self.password_entry: LoginPage.
                                 on_entry_click(e, self.password_placeholder))
        self.password_entry.bind('<FocusOut>', lambda event, e=self.password_entry: LoginPage.
                                 on_focusout(e, self.password_placeholder))
        self.password_entry.configure(fg='grey')
        self.password_entry.place(relx=0.45, rely=0.5, anchor="w")

        self.verify_password_entry = tk.Entry(self, fg="black", show="*", bg="#E0E0E0", borderwidth=0, relief="sunken")
        self.verify_password_entry.place(relx=0.45, rely=0.6, anchor="w")

        ttk.Button(self, text="Register", style='Transparent.TButton',
                   command=self.register_user).place(relx=0.5, rely=0.7, anchor="center")

    def register_user(self):
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
                self.controller.username = username
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
        self.resized_login_image = self.login_image.resize((1280, 680))
        self.login_background = ImageTk.PhotoImage(self.resized_login_image)
        canvas.create_image(640, 340, image=self.login_background)
        # draw text
        canvas.create_text(640, 200, text="Login", font="Helvetica 30 bold", fill="#FFE082")
        # configure style
        style = ttk.Style()
        style.theme_use('alt')
        style.configure('Transparent.TButton', borderwidth=0, padding=0)
        # a button to go back to the start page on the top left corner
        ttk.Button(self, text="Back", style='Transparent.TButton',
                   command=lambda: controller.show_frame("StartPage")).place(relx=0.1, rely=0.1, anchor="center")

        canvas.create_text(510, 270, text="Username:", font="Helvetica 20", fill="#FFE082")
        canvas.create_text(510, 340, text="Password:", font="Helvetica 20", fill="#FFE082")

        # Username entry
        self.username_placeholder = "genius user name"
        self.username_entry = tk.Entry(self, bg="#E0E0E0", border=0, relief="sunken")
        self.username_entry.insert(0, self.username_placeholder)

        self.username_entry.bind('<FocusIn>',
                                 lambda event, e=self.username_entry: self.on_entry_click(e, self.username_placeholder))
        self.username_entry.bind('<FocusOut>',
                                 lambda event, e=self.username_entry: self.on_focusout(e, self.username_placeholder))
        self.username_entry.configure(fg='grey')
        self.username_entry.place(relx=0.45, rely=0.4, anchor="w")

        # Password entry
        self.password_placeholder = "Password"
        self.password_entry = tk.Entry(self, show="*", bg="#E0E0E0", borderwidth=0, relief="sunken")
        self.password_entry.insert(0, self.password_placeholder)

        self.password_entry.bind('<FocusIn>',
                                 lambda event, e=self.password_entry: self.on_entry_click(e, self.password_placeholder))
        self.password_entry.bind('<FocusOut>',
                                 lambda event, e=self.password_entry: self.on_focusout(e, self.password_placeholder))
        self.password_entry.configure(fg='grey')
        self.password_entry.place(relx=0.45, rely=0.5, anchor="w")

        ttk.Button(self, text="Log In", style='Transparent.TButton',
                   command=self.attempt_login).place(relx=0.5, rely=0.6, anchor="center")

    # improve UI functions:

    @staticmethod
    def on_entry_click(entry, placeholder_text):
        """Function to be called when entry is clicked."""
        if entry.get() == placeholder_text:
            # delete all the text in the entry if the text is the placeholder text
            entry.delete(0, tk.END)
            entry.insert(0, '')
            entry.configure(fg='black')

    @staticmethod
    def on_focusout(entry, placeholder_text):
        """Function to be called when entry loses focus."""
        entry.configure(borderwidth=1,)
        if entry.get() == '':
            entry.insert(0, placeholder_text)
            entry.configure(fg='grey')

    def attempt_login(self):
        """this function will check if the username and password is correct or not"""
        # get the current username and password
        username = self.username_entry.get()
        password = self.password_entry.get()
        # call the check_password function
        if self.check_password(username, password):
            # messagebox.showinfo("Login Successful", "You have successfully logged in.")
            self.controller.show_frame("HomePage")
            self.controller.username = username
        else:
            messagebox.showerror("Login Failed", "Incorrect username or password.")
        # clear input fields after each attempt
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

    def check_password(self, username, password):
        # check if the username is in the database
        result = RegisterFunction.check_username(username)
        with open('encryption_key', 'r') as f:
            key = f.readline()
        # if the username is in the database, it will check if the password is correct or not
        if result and account_manager.decrypt(result[1], key) == password:
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

        # # a frame to display the books
        self.books_frame = tk.Frame(self)
        self.books_frame.pack(expand=True, fill="both", padx=20, pady=20)

        self.display_books()

    def display_books(self):
        # get all the books from the database
        # all_books = book_manager.search()
        # random_books = random.sample(all_books, min(len(all_books), 10))

        # get random books from the database by choosing a random page and a random entry
        random_books = book_manager.fetch_random_books(10)
        tk.Label(self.books_frame, text="   Books of The Day", font=("Helvetica", 20, "bold"), anchor="w").pack(
            fill="x", pady=(10, 20))

        for book in random_books:
            book_btn = ttk.Button(self.books_frame, text=f"•  {book.title} by {book.author} ({book.yearPublished})",
                                  style='Link.TButton',
                                  command=lambda b=book: self.show_book_info(b))
            book_btn.pack(fill='x', padx=20, pady=5)

    def show_book_info(self, book):
        # invoke the show_book function in the controller to tkraise the BookDetailsPage
        self.controller.show_book("BookDetailsPage", book)


# holder
Book1 = book_manager.Book("The Great Gatsby", "F. Scott Fitzgerald", 1925, "Scribner", "9780743273565", 5)


class BookDetailsPage(tk.Frame):
    """This page will display the details of a book. It will show the title,
    author, year published, publisher, and ISBN. Allowing the user to borrow or return the book in this page"""

    def __init__(self, parent, controller, book=Book1):
        super().__init__(parent)
        self.summaryLabel = None
        self.availabilityLabel = None
        self.summaryLabelRegular = None
        self.ratingLabel = None
        self.ratingLabelRegular = None
        self.publisherLabel = None
        self.publisherLabelRegular = None
        self.yearLabel = None
        self.yearLabelRegular = None
        self.ISBNLabel = None
        self.ISBNLabelRegular = None
        self.authorLabel = None
        self.authorLabelRegular = None
        self.titleLabel = None
        self.titleLabelRegular = None
        self.details_frame = None
        self.controller = controller
        self.book = book
        self.toolbar = CustomToolbar(self, controller)
        self.toolbar.pack(side="top", fill="x")
        tk.Label(self, text="Book Details", font=("Helvetica", 20, "bold")).pack(pady=10)

        # Display book information
        self.display_book_details()

        # check the current username logged in and try to display in the top left corner for later use
        # print(self.controller.username)

        # Borrow or return button
        # ------------------this may need to be updated (maybe only show the return button if its
        # borrowed instead of replacing it?-------------------------------------------
        if borrow_manager.borrowed(self.controller.username, self.book.ISBN):
            self.borrowReturnBtn = tk.Button(self, text="Return The Book", command=self.return_book)
            self.borrowReturnBtn.pack()
        else:
            self.borrowReturnBtn = tk.Button(self, text="Borrow", command=self.borrow_book)
            self.borrowReturnBtn.pack()
            if self.book.availability == 0:
                self.borrowReturnBtn["state"] = "disabled"
            else:
                self.borrowReturnBtn["state"] = "normal"

    def display_book_details(self):
        """Display book details on the page"""
        # get the summary and rating of the book from the google books api
        summary_rating = self.get_book_details(str(self.book.ISBN))
        summary, rating = summary_rating
        df_font = self.controller.db_font
        bd_font = self.controller.bd_FONT
        # details container frame
        self.details_frame = tk.Frame(self)
        self.details_frame.pack(fill='x', padx=10, pady=10)
        text_color = "#68fcf7"

        # Title
        self.titleLabelRegular = tk.Label(self.details_frame, text="Title: ", font=df_font)
        self.titleLabelRegular.pack(anchor='w')
        self.titleLabel = tk.Label(self.details_frame, text=f"{self.book.title}", font=bd_font, fg=text_color)
        self.titleLabel.pack(anchor='w')

        # Author
        self.authorLabelRegular = tk.Label(self.details_frame, text="Author: ", font=df_font)
        self.authorLabelRegular.pack(anchor='w')
        self.authorLabel = tk.Label(self.details_frame, text=f"{self.book.author}", font=bd_font, fg=text_color)
        self.authorLabel.pack(anchor='w')

        # ISBN
        self.ISBNLabelRegular = tk.Label(self.details_frame, text="ISBN: ", font=df_font)
        self.ISBNLabelRegular.pack(anchor='w')
        self.ISBNLabel = tk.Label(self.details_frame, text=f"{self.book.ISBN}", font=bd_font, fg=text_color)
        self.ISBNLabel.pack(anchor='w')

        # Year Published
        self.yearLabelRegular = tk.Label(self.details_frame, text="Year Published: ", font=df_font)
        self.yearLabelRegular.pack(anchor='w')
        self.yearLabel = tk.Label(self.details_frame, text=f"{self.book.yearPublished}", font=bd_font, fg=text_color)
        self.yearLabel.pack(anchor='w')

        # Publisher
        self.publisherLabelRegular = tk.Label(self.details_frame, text="Publisher: ", font=df_font)
        self.publisherLabelRegular.pack(anchor='w')
        self.publisherLabel = tk.Label(self.details_frame, text=f"{self.book.publisher}", font=bd_font, fg=text_color)
        self.publisherLabel.pack(anchor='w')

        # Rating
        self.ratingLabelRegular = tk.Label(self.details_frame, text="Rating: ", font=df_font)
        self.ratingLabelRegular.pack(anchor='w')
        self.ratingLabel = tk.Label(self.details_frame, text=f"{rating}", font=bd_font, fg=text_color)
        self.ratingLabel.pack(anchor='w')

        formatted_summary = summary[:1000] + "..." if len(summary) > 1000 else summary
        formatted_summary = "\n".join([formatted_summary[i:i + 180] for i in range(0, len(formatted_summary), 180)])

        self.summaryLabelRegular = tk.Label(self.details_frame, text="Summary: ", font=df_font)
        self.summaryLabelRegular.pack(anchor='w')
        self.summaryLabel = tk.Label(self.details_frame, text=f"{formatted_summary}", font=bd_font, justify='left',
                                     fg=text_color)
        self.summaryLabel.pack(anchor='w', expand=True)

        self.availabilityLabel = tk.Label(self.details_frame, text=f"Availability: {self.book.availability}",
                                          font=("Helvetica", 16))
        self.availabilityLabel.pack(anchor='e', pady=15, padx=15)

    def clear_book_details(self):
        """Clear book details from the page"""
        self.details_frame.pack_forget()

    def return_book(self):
        """Return the book and update the page"""
        borrow_manager.returnBook(self.controller.username, self.book.ISBN)
        # refresh details
        self.book = book_manager.getBookDetails(self.book.ISBN)
        self.clear_book_details()
        self.display_book_details()
        # change button (or maybe just hide the button if it's returned?, or show a message that it's returned)
        self.borrowReturnBtn.pack_forget()
        self.borrowReturnBtn = tk.Button(self, text="Borrow", command=self.borrow_book)
        self.borrowReturnBtn.pack()

    def borrow_book(self):
        borrow_manager.borrowBook(self.controller.username, self.book.ISBN)
        # refresh details
        self.book = book_manager.getBookDetails(self.book.ISBN)
        self.clear_book_details()
        self.display_book_details()
        # change button
        self.borrowReturnBtn.pack_forget()
        self.borrowReturnBtn = tk.Button(self, text="Return The Book", command=self.return_book)
        self.borrowReturnBtn.pack()

    @staticmethod
    # this function utilizes googlebooks api to get the book details
    def get_book_details(isbn: str) -> (str, int):
        # credit to https://www.datacamp.com/tutorial/making-http-requests-in-python
        # get the book details from the google books api
        url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                # Check if any books were found
                if data["totalItems"] > 0:
                    book_info = data["items"][0]["volumeInfo"]
                    summary = book_info.get("description", "No summary available")
                    rating = str(book_info.get("averageRating", "No rating available"))
                    return summary, rating
                else:
                    return "No results found", "N/A"
            else:
                return "Failed to fetch data", "N/A"
        except Exception:
            return "Data retrieval error", "N/A"


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
        search_btn = tk.Button(search_container, text='Search', command=self.new_search)
        search_btn.pack(side="left")

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
        page_container = tk.Frame(self)
        page_container.pack(side="top", fill="x", pady=5)
        self.prevPageBtn = tk.Button(page_container, text="<<<", command=self.prev_page, state="disabled")
        self.prevPageBtn.pack(side="left")
        self.pageNum = tk.Label(page_container, textvariable=self.pageVar, width=5)
        self.pageNum.pack(side="left")
        self.nextPageBtn = tk.Button(page_container, text=">>>", command=self.next_page, state="disabled")
        self.nextPageBtn.pack(side="left")
        self.paddingRight = tk.Label(page_container)
        self.paddingRight.pack(side="left", fill="x", expand=True)
        self.detailsBtn = tk.Button(page_container, text="Details", command=self.go_to_book_details)
        self.detailsBtn.pack(side="left")

    def new_search(self):
        """Reset page and search for books based on the search"""
        self.page = 1
        self.pageVar.set(str(self.page))
        self.search()

    def search(self):
        """Search for books based on the search criteria and display the results."""
        keyword = self.search_var.get()
        year_start = self.yearStartCombobox.get()
        year_end = self.yearEndCombobox.get()
        year_range = [year_start, year_end]
        if str(year_start) == "Any" and str(year_end) == "Any":
            year_range = None
        self.pageResults = book_manager.search(keyword, year_range, self.page)
        self.display_results()

        # Set page controls
        if self.page == 1:
            self.prevPageBtn["state"] = "disabled"
        else:
            self.prevPageBtn["state"] = "normal"
        if book_manager.search(keyword, year_range, self.page + 1):
            self.nextPageBtn["state"] = "normal"
        else:
            self.nextPageBtn["state"] = "disabled"

    def next_page(self):
        self.page += 1
        self.pageVar.set(str(self.page))
        self.search()

    def prev_page(self):
        self.page -= 1
        self.pageVar.set(str(self.page))
        self.search()

    def display_results(self):
        """Display search results in the treeview."""
        self.treeview.delete(*self.treeview.get_children())
        for result in self.pageResults:
            self.treeview.insert(
                "",
                tk.END,
                text=result.ISBN,
                values=(result.title, result.author, result.yearPublished, result.publisher)
            )

    def go_to_book_details(self):
        cur_item = self.treeview.item(self.treeview.focus())
        # print("focus(): ", self.treeview.focus())
        # print(curItem)
        if cur_item["text"]:
            book = book_manager.getBookDetails(cur_item["text"])
            self.controller.show_book("BookDetailsPage", book)


class BorrowedBooksPage(tk.Frame):
    """This page will display the books that the user has borrowed. It will show the title,
    author, date borrowed, and status."""

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.toolbar = CustomToolbar(self, controller)
        self.toolbar.pack(side="top", fill="x")
        df_font = self.controller.db_font
        self.loanPeriod = 21  # Set book loan period to 21 days

        tk.Label(self, text="Books Borrowed History", font=df_font).pack(pady=10)
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
        page_container = tk.Frame(self)
        page_container.pack(side="top", fill="x", pady=5)
        self.prevPageBtn = tk.Button(page_container, text="<<<", command=self.prev_page, state="disabled")
        self.prevPageBtn.pack(side="left")
        self.pageNum = tk.Label(page_container, textvariable=self.pageVar, width=5)
        self.pageNum.pack(side="left")
        self.nextPageBtn = tk.Button(page_container, text=">>>", command=self.next_page, state="disabled")
        self.nextPageBtn.pack(side="left")
        self.paddingRight = tk.Label(page_container)
        self.paddingRight.pack(side="left", fill="x", expand=True)
        self.detailsBtn = tk.Button(page_container, text="Details", command=self.go_to_book_details)
        self.detailsBtn.pack(side="left")

        self.pageResults = borrow_manager.getBorrowHistory(self.controller.username, self.page)
        # print(self.controller.username, self.page)
        # print(self.pageResults)
        self.display_results()

    def next_page(self):
        self.page += 1
        self.pageVar.set(str(self.page))
        self.pageResults = borrow_manager.getBorrowHistory(self.controller.username, self.page)
        self.display_results()

    def prev_page(self):
        self.page -= 1
        self.pageVar.set(str(self.page))
        self.pageResults = borrow_manager.getBorrowHistory(self.controller.username, self.page)
        self.display_results()

    def display_results(self):
        self.treeview.delete(*self.treeview.get_children())
        for result in self.pageResults:
            return_date = result.dateBorrowed + datetime.timedelta(days=self.loanPeriod)
            if not result.dateReturned:
                # check how long it's been since date borrowed
                if datetime.datetime.now() > return_date:
                    status = "OVERDUE"
                else:
                    status = "DUE ON " + return_date.strftime("%Y-%m-%d %H:%M:%S")
            else:
                if result.dateReturned > return_date:
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

    def go_to_book_details(self):
        cur_item = self.treeview.item(self.treeview.focus())
        # print("focus(): ", self.treeview.focus())
        # print(curItem)
        if cur_item["text"]:
            book = book_manager.getBookDetails(cur_item["text"])
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
        self.username_label = None
        self.password_label = None
        tk.Label(self, text="Account Page", font="Helvetica 30 bold").place(relx=0.5, rely=0.1, anchor="center")
        ttk.Button(self, text="Change Username", command=self.change_username).place(relx=0.5, rely=0.5,
                                                                                     anchor="center")
        ttk.Button(self, text="Change Password", command=self.change_password).place(relx=0.5, rely=0.55,
                                                                                     anchor="center")
        # ttk.Button(self, text="Logout", command=self.logout).place(relx=0.5, rely=0.6, anchor="center")

    # this function will display the current account information as username, password via the account_manager.py
    def display_account_info(self):
        # clear the previous account information
        if self.username_label:
            self.username_label.destroy()
        if self.password_label:
            self.password_label.destroy()

        if self.controller.username:
            username, password = account_manager.RegisterFunction.get_account(self.controller.username)
            # Display the account username and password as a label on the page
            self.username_label = tk.Label(self, text=f"Username: {username}",
                                           font=Font(family="Times New Roman", size=20, weight="bold"))
            self.username_label.place(relx=0.35, rely=0.3, anchor="w")
            self.password_label = tk.Label(self, text=f"Password: *****",
                                           font=Font(family="Times New Roman", size=20, weight="bold"))
            self.password_label.place(relx=0.35, rely=0.4, anchor="w")
            # a show button to show the password
            ttk.Button(self, text="Show Password", command=lambda: self.show_password(password)).place(relx=0.7,
                                                                                                       rely=0.4,
                                                                                                       anchor="center")

    # only show the password in plaintext if the user clicks the show password button
    def show_password(self, password):
        if self.password_label:
            self.password_label.destroy()

        password = account_manager.decrypt(password, account_manager.key)
        self.password_label = tk.Label(self, text=f"Password: {password}",
                                       font=Font(family="Times New Roman", size=20, weight="bold"))
        self.password_label.place(relx=0.35, rely=0.4, anchor="w")

    # this function allows the user to modify the password via the account_manager.py
    def change_password(self):
        if self.controller.username:
            username, password = account_manager.RegisterFunction.get_account(self.controller.username)
            # ask the user to enter the new password
            new_password = simpledialog.askstring("Input", "Enter the new password", parent=self)
            # if the user entered the new password
            if new_password:
                # update the password
                account_manager.RegisterFunction.update_password(username, new_password)
                new_password = account_manager.encrypt(new_password, account_manager.key)
                self.controller.password = new_password
                messagebox.showinfo("Success", "Password updated successfully")
                self.display_account_info()
                self.show_password(new_password)

    # this function allows the user to modify the username via the account_manager.py
    def change_username(self):
        if self.controller.username:
            username, password = account_manager.RegisterFunction.get_account(self.controller.username)
            # ask the user to enter the new username
            new_username = simpledialog.askstring("Input", "Enter the new username", parent=self)
            # check if new username exists
            if account_manager.RegisterFunction.check_username(new_username):
                messagebox.showerror("Username Change Failed", "Username is already taken.")
                return
            # if the user entered the new username
            if new_username:
                # update the username
                # transfer the borrowed books to the new username
                borrow_manager.transferBorrow(username, new_username)
                account_manager.RegisterFunction.update_username(username, new_username)
                self.controller.username = new_username
                messagebox.showinfo("Success", "Username updated successfully")
                self.display_account_info()


class RecommendPage(tk.Frame):
    # for books suggestions based on user's borrowing history
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # put the toolbar on the top of the page
        self.toolbar = CustomToolbar(self, controller)
        self.toolbar.pack(side="top", fill="x")

        # Placeholder for recommended books display
        self.books_frame = tk.Frame(self)
        self.books_frame.pack(expand=True, fill="both", padx=20, pady=20)

        self.display_recommendations()

        
    def display_recommendations(self):
        # Fetch the most recent borrowed book for the current user
        recent_book = borrow_manager.get_most_recent_borrowed_book(self.controller.username)
        if recent_book:
            # If there's a recent book, use its author for recommendations
            author_name = recent_book.author
            recommended_books = book_manager.fetch_random_books_by_author(author_name, 10)
            tk.Label(self.books_frame, text="   Books Recommended", font=("Helvetica", 20, "bold"), anchor="w").pack(fill="x", pady=(10, 20))
            for book in recommended_books:
                book_btn = ttk.Button(self.books_frame, text=f"•  {book.title} by {book.author} ({book.yearPublished})", style='Link.TButton', command=lambda b=book: self.show_book_info(b))
                book_btn.pack(fill='x', padx=20, pady=5)
        else:
            # If there's no borrowed book, use random
            random_books = book_manager.fetch_random_books(10)
            tk.Label(self.books_frame, text="   Books Recommended", font=("Helvetica", 20, "bold"), anchor="w").pack(
                fill="x", pady=(10, 20))

            for book in random_books:
                book_btn = ttk.Button(self.books_frame, text=f"•  {book.title} by {book.author} ({book.yearPublished})",
                                      style='Link.TButton',
                                      command=lambda b=book: self.show_book_info(b))
                book_btn.pack(fill='x', padx=20, pady=5)


    def show_book_info(self, book):
        # invoke the show_book function in the controller to tkraise the BookDetailsPage
        self.controller.show_book("BookDetailsPage", book)



class CustomToolbar(tk.Frame):
    """This is a custom toolbar that will be displayed on the top of the page.
    It will have the home button, account menu,
    Search Button icon from: https://www.shareicon.net/loop-view-magnifier-zoom-
    search-eye-research-magnifying-glass-explore-magnifying-find-glass-82290"""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.search_icon = tk.PhotoImage(file="assets/search.png")
        # home page button
        tk.Button(self, text="Home", command=lambda: controller.show_frame("HomePage")).pack(side="left", padx=10,
                                                                                             pady=10)
        # account menu
        account_menu = tk.Menubutton(self, text="Account", relief=tk.RAISED)
        account_menu.menu = tk.Menu(account_menu, tearoff=0)
        account_menu["menu"] = account_menu.menu

        account_menu.menu.add_command(label="Account Setting", command=lambda: [self.update_account_page(),
                                                                                controller.show_frame("AccountPage")])
        account_menu.menu.add_command(label="Borrowed Books",
                                      command=lambda: controller.show_borrow_history("BorrowedBooksPage"))
        account_menu.menu.add_command(label="Recommendation", command=lambda: controller.show_frame("RecommendPage"))
        account_menu.menu.add_command(label="Log out", command=lambda: controller.show_frame("StartPage"))
        # debug
        # account_menu.menu.add_command(label="show", command=self.show_account)

        account_menu.pack(side="right", padx=10, pady=10)

        # Search Button
        tk.Button(self, image=self.search_icon, command=lambda: controller.show_frame("SearchPage")).pack(side="right",
                                                                                                          padx=10,
                                                                                                          pady=10)
        # Accessibility Menu
        accessibility_menu = tk.Menubutton(self, text="Accessibility", relief=tk.RAISED)
        accessibility_menu.menu = tk.Menu(accessibility_menu, tearoff=0)
        accessibility_menu["menu"] = accessibility_menu.menu
        accessibility_menu.pack(side="right", padx=10, pady=10)

        # Colour menu
        colour_menu = tk.Menu(accessibility_menu.menu, tearoff=0)
        colour_menu.add_command(label="High Contrast", command=lambda: self.change_colour("high_contrast"))
        colour_menu.add_command(label="Black & White", command=lambda: self.change_colour("normal"))
        accessibility_menu.menu.add_cascade(label="Colour", menu=colour_menu)

    # debug
    def update_account_page(self):
        AccountPage.display_account_info(self.controller.frames["AccountPage"])

    def change_colour(self, theme):
        """for accessibility, change the colour of the text and buttons for better readability"""
        if theme == "high_contrast":
            background_color = "red"
            text_color = "blue"
            button_color = "red"
        elif theme == "normal":
            # default colours
            background_color = "SystemButtonFace"
            text_color = "black"
            button_color = "SystemButtonFace"

        # apply colors to tkinter widgets
        for widget in self.controller.walk_widgets():
            if isinstance(widget, tk.Label) or isinstance(widget, tk.Entry):
                widget.config(background=background_color, foreground=text_color)
            elif isinstance(widget, tk.Button):
                widget.config(background=button_color, foreground=text_color, activebackground=button_color)

        # apply colors to ttk widgets
        style = ttk.Style()
        style.configure("TLabel", background=background_color, foreground=text_color)
        style.configure("TButton", background=button_color, foreground=text_color)
        style.configure("TEntry", fieldbackground=background_color, foreground=text_color)
        style.map("TButton", background=[("active", button_color)], foreground=[("active", text_color)])
