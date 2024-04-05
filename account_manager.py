import sqlite3
import bcrypt

class RegisterFunction():
    @staticmethod
    def create_table():
        conn = sqlite3.connect('library.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS account
                     (username TEXT PRIMARY KEY NOT NULL,
                      password TEXT NOT NULL)''')
        conn.commit()
        conn.close()
    @staticmethod
    def insert_account(username, password):
        conn = sqlite3.connect('library.db')
        c = conn.cursor()
        c.execute("INSERT INTO account (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()


    @staticmethod
    def check_username(username):
        conn = sqlite3.connect('library.db')
        c = conn.cursor()
        c.execute("SELECT * FROM account WHERE username = ?", (username,))
        result = c.fetchone()
        conn.close()
        return result

    # this function allows the user to modify their Username only
    @staticmethod
    def update_username(username, new_username):
        conn = sqlite3.connect('library.db')
        c = conn.cursor()
        c.execute("UPDATE account SET username = ? WHERE username = ?", (new_username, username))
        conn.commit()
        conn.close()


    # this function allows the user to modify their Password only
    @staticmethod
    def update_password(username, new_password):
        conn = sqlite3.connect('library.db')
        c = conn.cursor()
        c.execute("UPDATE account SET password = ? WHERE username = ?", (new_password, username))
        conn.commit()
        conn.close()

    # this function returns the username and password of the user
    @staticmethod
    def get_account(username):
        conn = sqlite3.connect('library.db')
        c = conn.cursor()
        c.execute("SELECT * FROM account WHERE username = ?", (username,))
        result = c.fetchone()
        conn.close()
        return result

