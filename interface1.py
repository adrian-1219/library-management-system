import tkinter as tk
from tkinter import ttk, messagebox
#from PIL import ImageTk, Image
import sqlite3
#from tkinter import *


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Library')
        self.geometry('680x480')

        self.container = tk.Frame(self)
        self.container.pack(expand=True, fill="both", padx=20, pady=20)

        self.frames = {}

        for F in (StartPage, RegisterPage, LoginPage, HomePage, SearchPage): 
            frame = F(parent=self.container, controller=self)
            self.frames[F] = frame
            frame.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
    
    def add_menu(self, frame):
        menu_bar = tk.Menu(frame)
        self.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Help", menu=file_menu)
        file_menu.add_command(label="Start Page", command=lambda: self.show_frame(StartPage))
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        # library label
        tk.Label(self, text="Library", font=("Helvetica", 30)).place(relx=0.5, rely=0.2, anchor="center")

        # register/login buttons
        ttk.Button(self, text="Register",
                   command=lambda: controller.show_frame(RegisterPage)).place(relx=0.5, rely=0.4, anchor="center")
        ttk.Button(self, text="Login",
                   command=lambda: controller.show_frame(LoginPage)).place(relx=0.5, rely=0.5, anchor="center")

class RegisterFunction():
    def create_table():
        conn = sqlite3.connect('account.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS account
                    (username TEXT PRIMARY KEY NOT NULL,
                    password TEXT NOT NULL)''')
        conn.commit()
        conn.close()

    def insert_account(username, password):
        conn = sqlite3.connect('account.db')
        c = conn.cursor()
        c.execute("INSERT INTO account (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close() 

    def check_username(username):
        conn = sqlite3.connect('account.db')
        c = conn.cursor()
        c.execute("SELECT * FROM account WHERE username = ?", (username,))
        result = c.fetchone()
        conn.close()
        return result
    
class RegisterPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        controller.add_menu(self)

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
        username = self.username_entry.get()  # Use .get() to fetch the entry's text
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
                self.controller.show_frame(HomePage)    

class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        controller.add_menu(self)
        
        tk.Label(self, text="Login").place(relx=0.5, rely=0.3, anchor="center")
        
        username_label = tk.Label(self, text="Username")
        username_label.place(relx=0.4, rely=0.4, anchor="e")
        username_entry = ttk.Entry(self)
        username_entry.place(relx=0.4, rely=0.4, anchor="w")

        password_label = tk.Label(self, text="Password")
        password_label.place(relx=0.4, rely=0.5, anchor="e")
        password_entry = ttk.Entry(self, show="*")
        password_entry.place(relx=0.4, rely=0.5, anchor="w")

        ttk.Button(self, text="Login",
                   command=lambda: controller.show_frame(HomePage)).place(relx=0.5, rely=0.6, anchor="center")

    def not_find(self):
        username = username_entry.get()
        password = password_entry.get()

        result_n = RegisterFunction.check_username(username)
        result_p = RegisterFunction.check_username(password)

        if result_n and result_p:
            messagebox.showinfo('Success', 'Login successfully')
            self.controller.show_frame(HomePage)
        else:
            messagebox.showinfo('Error', 'Login failed, please create an account or check password')

        
class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        tk.Label(self, text="Welcome to the Library", font=("Helvetica", 20)).place(relx=0.5, rely=0.3, anchor="center")

        self.toolbar = CustomToolbar(self, controller)
        self.toolbar.pack(side="top", fill="x")
        
        # Example of a logout button to return to the StartPage
        ttk.Button(self, text="Logout",
                command=lambda: controller.show_frame(StartPage)).place(relx=0.5, rely=0.5, anchor="center")


class CustomToolbar(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.search_icon = tk.PhotoImage(file="search.png")

        # home page button
        tk.Button(self, text="Home", command=lambda: controller.show_frame(HomePage)).pack(side="left", padx=10)

        # account menu
        account_menu = tk.Menubutton(self, text="Account", relief=tk.RAISED)
        account_menu.menu = tk.Menu(account_menu, tearoff=0)
        account_menu["menu"] = account_menu.menu
        account_menu.menu.add_command(label="Account Page", command=lambda: controller.show_frame(AccountPage))
        account_menu.menu.add_command(label="Borrowed", command=lambda: controller.show_frame(BorrowedBooksPage))
        account_menu.menu.add_command(label="Log out", command=lambda: controller.show_frame(StartPage))
        account_menu.pack(side="right", padx=10)

        # Search Button
        tk.Button(self, image=self.search_icon, command=lambda: controller.show_frame(SearchPage)).pack(side="right", padx=10)

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

    def perform_search(self):
        search_query = self.search_entry.get()
        pass

class BorrowedBooksPage():
    pass
class AccountPage():
    pass




if __name__ == "__main__":
    RegisterFunction.create_table()
    app = App()
    app.mainloop()

