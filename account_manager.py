import sqlite3

class RegisterFunction():
    @staticmethod
    def create_table():
        conn = sqlite3.connect('account.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS account
                     (username TEXT PRIMARY KEY NOT NULL,
                      password TEXT NOT NULL)''')
        conn.commit()
        conn.close()

    @staticmethod
    def insert_account(username, password):
        conn = sqlite3.connect('account.db')
        c = conn.cursor()
        c.execute("INSERT INTO account (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()

    @staticmethod
    def check_username(username):
        conn = sqlite3.connect('account.db')
        c = conn.cursor()
        c.execute("SELECT * FROM account WHERE username = ?", (username,))
        result = c.fetchone()
        conn.close()
        return result
