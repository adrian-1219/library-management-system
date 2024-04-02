import tkinter as tk
from tkinter import ttk, messagebox
from account_manager import RegisterFunction
import models, datetime


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
        self.page = 1
        self.pageVar = tk.StringVar()
        self.pageVar.set(str(self.page))

        self.toolbar = CustomToolbar(self, controller)
        self.toolbar.pack(side="top", fill="x")

        # Container Frame for search
        search_container = tk.Frame(self)
        search_container.pack(side="top", fill="x", padx=10, pady=10)

        # Year range selection for search
        print(datetime.date.today())
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
        self.paddingLeft = tk.Label(pageContainer)
        self.paddingLeft.pack(side="left", fill="x", expand=True)
        self.prevPageBtn = tk.Button(pageContainer, text="<<<", command=self.prevPage, state="disabled")
        self.prevPageBtn.pack(side="left")
        self.pageNum = tk.Label(pageContainer, textvariable=self.pageVar, width=5)
        self.pageNum.pack(side="left")
        self.nextPageBtn = tk.Button(pageContainer, text=">>>", command=self.nextPage, state="disabled")
        self.nextPageBtn.pack(side="left")
        self.paddingRight = tk.Label(pageContainer)
        self.paddingRight.pack(side="left", fill="x", expand=True)

    def newSearch(self):
        self.page = 1 
        self.pageVar.set(str(self.page))
        self.search()

    def search(self):
        keyword = self.search_var.get()
        yearStart = self.yearStartCombobox.get()
        yearEnd = self.yearEndCombobox.get()
        yearRange = [yearStart, yearEnd]
        if str(yearStart) == "Any" and str(yearEnd) == "Any":
            yearRange = None
        self.pageResults = models.search(keyword, yearRange, self.page)
        self.displayResults()

        # Set page controls
        if self.page == 1:
            self.prevPageBtn["state"] = "disabled"
        else:
            self.prevPageBtn["state"] = "normal"
        if models.search(keyword, yearRange, self.page + 1):
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
    def __init__(self, parent, controller, username):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.username = username

        tk.Label(self, text="Account Page", font=("Helvetica", 20)).place(relx=0.5, rely=0.1, anchor="center")
        tk.Label(self, text="Username:").place(relx=0.3, rely=0.3, anchor="e")
        tk.Label(self, text=username).place(relx=0.35, rely=0.3, anchor="w")

        tk.Label(self, text="Password:").place(relx=0.3, rely=0.4, anchor="e")
        password = self.get_password(username)
        tk.Label(self, text=password).place(relx=0.35, rely=0.4, anchor="w")

        ttk.Button(self, text="Modify Username", command=self.modify_username).place(relx=0.5, rely=0.5,
                                                                                     anchor="center")
        ttk.Button(self, text="Modify Password", command=self.modify_password).place(relx=0.5, rely=0.6,
                                                                                     anchor="center")
        ttk.Button(self, text="Modify Email", command=self.modify_email).place(relx=0.5, rely=0.7,
                                                                               anchor="center")
        ttk.Button(self, text="Logout", command=self.logout).place(relx=0.5, rely=0.8, anchor="center")

    def get_password(self, username):
        conn = sqlite3.connect('account.db')
        c = conn.cursor()
        c.execute("SELECT password FROM account WHERE username = ?", (username,))
        result = c.fetchone()
        conn.close()
        return result[0] if result else ""

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

    def modify_password(self):
        new_password = simpledialog.askstring("Input", "Enter new password:", parent=self)
        if new_password:
            conn = sqlite3.connect('account.db')
            c = conn.cursor()
            c.execute("UPDATE account SET password = ? WHERE username = ?", (new_password, self.username))
            conn.commit()
            conn.close()
            messagebox.showinfo('Success', 'Password modified successfully')

    def modify_email(self):
        new_email = simpledialog.askstring("Input", "Enter new email:", parent=self)
        if new_email:
            conn = sqlite3.connect('account.db')
            c = conn.cursor()
            c.execute("UPDATE account SET email = ? WHERE username = ?", (new_email, self.username))
            conn.commit()
            conn.close()
            messagebox.showinfo('Success', 'Email modified successfully')

    def logout(self):
        RegisterFunction.delete_account(self.username)
        messagebox.showinfo('Success', 'Account deleted successfully')
        self.controller.show_frame(StartPage)

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
