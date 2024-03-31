
import sqlite3
from tkinter import *
from tkinter import messagebox


# create a database and table to store user account information
def create_table():
    conn = sqlite3.connect('account.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS account
                 (username TEXT PRIMARY KEY NOT NULL,
                 password TEXT NOT NULL)''')
    conn.commit()
    conn.close()


# insert user account information into the table
def insert_account(username, password):
    conn = sqlite3.connect('account.db')
    c = conn.cursor()
    c.execute("INSERT INTO account (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()


# check if the username already exists in the table
def check_username(username):
    conn = sqlite3.connect('account.db')
    c = conn.cursor()
    c.execute("SELECT * FROM account WHERE username = ?", (username,))
    result = c.fetchone()
    conn.close()
    return result

# register an account

def register():
    username = entry1.get()
    password = entry2.get()
    if username == '' or password == '':
        messagebox.showinfo('Error', 'Please enter username and password')
    else:
        result = check_username(username)
        if result:
            messagebox.showinfo('Error', 'Username already exists')
        else:
            insert_account(username, password)
            messagebox.showinfo('Success', 'Account registered successfully')
            entry1.delete(0, END)
            entry2.delete(0, END)


def register_account():
    global entry1, entry2
    root = Tk()
    root.title('Register Account')
    root.geometry('300x200')
    label1 = Label(root, text='Username:')
    label1.pack()
    entry1 = Entry(root)
    entry1.pack()
    label2 = Label(root, text='Password:')
    label2.pack()
    entry2 = Entry(root, show='*')
    entry2.pack()
    button = Button(root, text='Register', command=register)
    button.pack()
    root.mainloop()


if __name__ == '__main__':
    create_table()
    register_account()


