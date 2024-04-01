import tkinter as tk
from tkinter import ttk, messagebox
from account_manager import RegisterFunction
import models


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Library Management System", font=("Helvetica", 30)).place(relx=0.5, rely=0.2, anchor="center")
        ttk.Button(self, text="Register", command=lambda: controller.show_frame("RegisterPage")).place(relx=0.5, rely=0.4, anchor="center")
        ttk.Button(self, text="Login", command=lambda: controller.show_frame("LoginPage")).place(relx=0.5, rely=0.5, anchor="center")


class RegisterPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        tk.Label(self, text="Register").place(relx=0.5, rely=0.2, anchor="center")
        username_label = tk.Label(self, text="Username")
        username_label.place(relx=0.4, rely=0.3, anchor="e")
        self.username_entry = ttk.Entry(self)
        self.username_entry.place(relx=0.4, rely=0.3, anchor="w")

        password_label = tk.Label(self, text="Password")
        password_label.place(relx=0.4, rely=0.4, anchor="e")
        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.place(relx=0.4, rely=0.4, anchor="w")

        verify_password_label = tk.Label(self, text="Verify Password")
        verify_password_label.place(relx=0.4, rely=0.5, anchor="e")
        self.verify_password_entry = ttk.Entry(self, show="*")
        self.verify_password_entry.place(relx=0.4, rely=0.5, anchor="w")

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
            # Your registration logic here


class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        controller.add_menu(self)
        tk.Label(self, text="Login").place(relx=0.5, rely=0.3, anchor="center")

        username_label = tk.Label(self, text="Username: ")
        username_label.place(relx=0.45, rely=0.4, anchor="e")
        username_entry = ttk.Entry(self)
        username_entry.place(relx=0.45, rely=0.4, anchor="w")

        password_label = tk.Label(self, text="Password: ")
        password_label.place(relx=0.45, rely=0.5, anchor="e")
        password_entry = ttk.Entry(self, show="*")
        password_entry.place(relx=0.45, rely=0.5, anchor="w")

        ttk.Button(self, text="Login",
                   command=lambda: controller.show_frame("HomePage")).place(relx=0.5, rely=0.6, anchor="center")

    # Login logic here


class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Welcome to the Library", font=("Helvetica", 20)).place(relx=0.5, rely=0.3, anchor="center")
        self.toolbar = CustomToolbar(self, controller)
        self.toolbar.pack(side="top", fill="x")

        # Example of a logout button to return to the StartPage
        ttk.Button(self, text="Logout",
                   command=lambda: controller.show_frame("StartPage")).place(relx=0.5, rely=0.5, anchor="center")


class SearchPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.pageResults = []

        self.toolbar = CustomToolbar(self, controller)
        self.toolbar.pack(side="top", fill="x")

        # Container Frame for search
        search_container = tk.Frame(self)
        search_container.pack(side="top", fill="x", padx=10, pady=10)

        # Search Entry
        self.search_var = tk.StringVar()
        self.searchEntry = tk.Entry(search_container, textvariable=self.search_var)
        self.searchEntry.pack(side="left", expand=True, fill="x", padx=(0, 5))

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
        self.pageResults = models.search(keyword)
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


class BorrowedBooksPage(tk.Frame):
    # Placeholder for BorrowedBooksPage
    pass


class AccountPage(tk.Frame):
    # Placeholder for AccountPage and Borrowed books details go in this page
    pass

class RecommendPage(tk.Frame):
    # for books suggestions based on user's borrowing history
    pass


class CustomToolbar(tk.Frame):
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
        account_menu.menu.add_command(label="Borrowed Books", command=lambda: controller.show_frame("BorrowedBooksPage"))
        account_menu.menu.add_command(label="Recommendation", command=lambda: controller.show_frame("RecommendPage"))
        account_menu.menu.add_command(label="Log out", command=lambda: controller.show_frame("StartPage"))
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
