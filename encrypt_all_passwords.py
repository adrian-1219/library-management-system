# This script encrypts all passwords in library.db. This was used to encrypt existing passwords before it was
# implemented in account creation and password updates.

from cryptography.fernet import Fernet
import sqlite3

def encrypt(password, key):
    et = Fernet(key).encrypt(password.encode()) 
    return et.decode()

def decrypt(encryptedPassword, key):
    dt = Fernet(key).decrypt(encryptedPassword)
    return dt.decode()

with open('encryption_key', 'r') as f:
    key = f.readline()

conn = sqlite3.connect('library.db')
c = conn.cursor()
c.execute('''SELECT * FROM account''')
accounts = c.fetchall()
for account in accounts:
    username = account[0]
    password = account[1]
    encryptedPass = encrypt(password, key)
    c.execute('''UPDATE account SET password = ?''', (encryptedPass,))
conn.commit()
conn.close()

