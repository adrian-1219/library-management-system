import tkinter as tk
import random
from tkinter import ttk, messagebox
from account_manager import RegisterFunction
<<<<<<< Updated upstream
=======
import books_manager
>>>>>>> Stashed changes


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Library", font=("Helvetica", 30)).place(relx=0.5, rely=0.2, anchor="center")
        ttk.Button(self, text="Register", command=lambda: controller.show_frame("RegisterPage")).place(relx=0.5, rely=0.4, anchor="center")
        ttk.Button(self, text="Login", command=lambda: controller.show_frame("LoginPage")).place(relx=0.5, rely=0.5, anchor="center")


class RegisterPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        tk.Label(self, text="Register").place(relx=0.5, rely=0.2, anchor="center")
        username_label = tk.Label(self, text="Username")
        username_label.place(relx=0.45, rely=0.3, anchor="e")
        self.username_entry = ttk.Entry(self)
        self.username_entry.place(relx=0.45, rely=0.3, anchor="w")

        password_label = tk.Label(self, text="Password")
        password_label.place(relx=0.45, rely=0.4, anchor="e")
        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.place(relx=0.45, rely=0.4, anchor="w")

        verify_password_label = tk.Label(self, text="Verify Password")
        verify_password_label.place(relx=0.45, rely=0.5, anchor="e")
        self.verify_password_entry = ttk.Entry(self, show="*")
        self.verify_password_entry.place(relx=0.45, rely=0.5, anchor="w")

        ttk.Button(self, text="Submit",
                   command=self.register).place(relx=0.5, rely=0.6, anchor="center")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        v_password = self.verify_password_entry.get()

        if username == '' or password == '':
            messagebox.showinfo('Error', 'Please enter username and password')
        elif password != v_password:
            messagebox.showinfo('Error', 'Please check the password')
        else:
            result = RegisterFunction.check_username(username)
            if result:
                messagebox.showinfo('Error', 'Username already exists')
            else:
                RegisterFunction.insert_account(username, password)  # Use class name to call static method
                messagebox.showinfo('Success', 'Account registered successfully')
                self.username_entry.delete(0, tk.END)
                self.password_entry.delete(0, tk.END)
                self.controller.show_frame("HomePage")


class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        controller.add_menu(self)
        tk.Label(self, text="Login").place(relx=0.5, rely=0.3, anchor="center")

<<<<<<< Updated upstream
        username_label = tk.Label(self, text="Username")
        username_label.place(relx=0.4, rely=0.4, anchor="e")
        username_entry = ttk.Entry(self)
        username_entry.place(relx=0.4, rely=0.4, anchor="w")

        password_label = tk.Label(self, text="Password")
        password_label.place(relx=0.4, rely=0.5, anchor="e")
        password_entry = ttk.Entry(self, show="*")
        password_entry.place(relx=0.4, rely=0.5, anchor="w")
=======
        username_label = tk.Label(self, text="Username: ")
        username_label.place(relx=0.45, rely=0.4, anchor="e")
        self.username_entry = ttk.Entry(self)  # Make it an instance variable
        self.username_entry.place(relx=0.45, rely=0.4, anchor="w")

        password_label = tk.Label(self, text="Password: ")
        password_label.place(relx=0.45, rely=0.5, anchor="e")
        self.password_entry = ttk.Entry(self, show="*")  # Make it an instance variable
        self.password_entry.place(relx=0.45, rely=0.5, anchor="w")
>>>>>>> Stashed changes

        ttk.Button(self, text="Login",
                   command=self.attempt_login).place(relx=0.5, rely=0.6, anchor="center")

    def attempt_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.check_password(username, password):
            messagebox.showinfo("Login Successful", "You have successfully logged in.")
            self.controller.show_frame("HomePage")
        else:
            messagebox.showerror("Login Failed", "Incorrect username or password.")

    def check_password(self, username, password):
        result = RegisterFunction.check_username(username)
        if result and result[1] == password:
            self.controller.current_account = username
            return True
        return False

    def logout(self):
        self.controller.current_account = None
        messagebox.showinfo("Logout Successful", "You have been logged out.")
        self.controller.show_frame("StartPage")


class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        tk.Label(self, text="Welcome to the Library", font=("Helvetica", 25, "bold")).place(relx=0.5, rely=0.3, anchor="center")
        self.toolbar = CustomToolbar(self, controller)
        self.toolbar.pack(side="top", fill="x")

        self.books_frame = tk.Frame(self)
        self.books_frame.pack(expand=True, fill="both", padx=20, pady=20)

        self.display_books()
        # ttk.Button(self, text="Logout",
        #            command=lambda: controller.show_frame("StartPage")).place(relx=0.5, rely=0.5, anchor="center")

    # a function to display random 10 books from the database
    def display_books(self):
        all_books = books_manager.search()  # Assuming this fetches all books
        random_books = random.sample(all_books, min(len(all_books), 10))
        tk.Label(self.books_frame, text="   Books of the day", font=("Helvetica", 20, "bold"), anchor="w").pack(fill="x", pady=(10, 20))

        for book in random_books:
            book_btn = ttk.Button(self.books_frame, text=f"•  {book.title} by {book.author} ({book.yearPublished})",
                                  style='Link.TButton',
                                  command=lambda b=book: self.show_book_info(b))
            book_btn.pack(fill='x', padx=20, pady=5)

    def show_book_info(self, book):
        self.controller.show_book("BookDetailsPage", book)


class BookDetailsPage(tk.Frame):
    def __init__(self, parent, controller, book):
        super().__init__(parent)
        self.controller = controller
        self.book = book
        self.toolbar = CustomToolbar(self, controller)
        self.toolbar.pack(side="top", fill="x")

        tk.Label(self, text="Book Details", font=("Helvetica", 20, "bold")).pack(pady=10)

        # Display book information
        tk.Label(self, text=f"Title: {self.book.title}", font=("Helvetica", 16)).pack()
        tk.Label(self, text=f"Author: {self.book.author}", font=("Helvetica", 16)).pack()
        tk.Label(self, text=f"ISBN: {self.book.ISBN}", font=("Helvetica", 16)).pack()
        tk.Label(self, text=f"Year Published: {self.book.yearPublished}", font=("Helvetica", 16)).pack()
        tk.Label(self, text=f"Publisher: {self.book.publisher}", font=("Helvetica", 16)).pack()




class SearchPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        search_frame = tk.Frame(self)
        search_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.search_entry = ttk.Entry(search_frame, width=50)
        self.search_entry.pack(side="left")

        search_button = ttk.Button(search_frame, text="Search", command=self.perform_search)
        search_button.pack(side="left", padx=(5,0))

<<<<<<< Updated upstream
    def perform_search(self):
        search_query = self.search_entry.get()
        pass
=======
        # Search Button
        searchBtn = tk.Button(search_container, text='Search', command=self.search)
        searchBtn.pack(side="left")

        self.treeview = ttk.Treeview(self, columns=("title", "author", "year", "publisher"))
        self.treeview.heading("#0", text="ISBN")
        self.treeview.heading("title", text="Title")
        self.treeview.heading("author", text="Author")
        self.treeview.heading("year", text="Year")
        self.treeview.heading("publisher", text="Publisher")
        self.treeview.pack(side="top", expand=True, fill="both", padx=10, pady=(5, 0))


    def search(self):
        keyword = self.search_var.get()
        self.pageResults = books_manager.search(keyword)
        self.displayResults()

    def displayResults(self):
        self.treeview.delete(*self.treeview.get_children())
        for result in self.pageResults:
            self.treeview.insert(
                "",
                tk.END,
                text=result.ISBN,
                values=(result.title, result.author, result.yearPublished, result.publisher)
            )
>>>>>>> Stashed changes


class BorrowedBooksPage(tk.Frame):
    # Placeholder for BorrowedBooksPage
    pass


class AccountPage(tk.Frame):
    # Placeholder for AccountPage
    pass


class CustomToolbar(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.search_icon = tk.PhotoImage(file="assets/search.png")

        # home page button
        tk.Button(self, text="Home", command=lambda: controller.show_frame("HomePage")).pack(side="left", padx=10)

        # create a lable that shows the account name of the user that is logged in
        tk.Label(self, text=controller.current_account, font=("Helvetica", 12)).pack(side="left", padx=14)
        print(controller.current_account)

        # account menu
        account_menu = tk.Menubutton(self, text="Account", relief=tk.RAISED)
        account_menu.menu = tk.Menu(account_menu, tearoff=0)
        account_menu["menu"] = account_menu.menu
<<<<<<< Updated upstream
        account_menu.menu.add_command(label="Account Page", command=lambda: controller.show_frame(AccountPage))
        account_menu.menu.add_command(label="Borrowed", command=lambda: controller.show_frame(BorrowedBooksPage))
        account_menu.menu.add_command(label="Log out", command=lambda: controller.show_frame(StartPage))
=======
        account_menu.menu.add_command(label="Account Setting", command=lambda: controller.show_frame("AccountPage"))
        account_menu.menu.add_command(label="Borrowed Books", command=lambda: controller.show_frame("BorrowedBooksPage"))
        account_menu.menu.add_command(label="Recommendation", command=lambda: controller.show_frame("RecommendPage"))
        account_menu.menu.add_command(label="Log out", command=lambda: controller.logout())

>>>>>>> Stashed changes
        account_menu.pack(side="right", padx=10)

        # Search Button
        tk.Button(self, image=self.search_icon, command=lambda: controller.show_frame("SearchPage")).pack(side="right", padx=10)

        # Accessibility Menu
        accessibility_menu = tk.Menubutton(self, text="Accessibility", relief=tk.RAISED)
        accessibility_menu.menu = tk.Menu(accessibility_menu, tearoff=0)
        accessibility_menu["menu"] = accessibility_menu.menu
        accessibility_menu.menu.add_command(label="Font", command=self.change_font)
        accessibility_menu.menu.add_command(label="Colour", command=self.change_colour)
        accessibility_menu.pack(side="right", padx=10)

    def change_font(self):
        pass

    def change_colour(self):
        pass
