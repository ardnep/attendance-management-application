import sqlite3
import hashlib
import os


class DbManager:
    @staticmethod
    def check_db():
        if not os.path.isfile('user_info.db'):  # checking if the list returned is empty
            DbManager.init_user_db()
        return True

    @staticmethod
    def connect_user_db():
        conn = sqlite3.connect('user_info.db')
        c = conn.cursor()

        return conn, c

    @staticmethod
    def init_user_db():
        conn, c = DbManager.connect_user_db()

        c.execute('''CREATE TABLE users
        (id INTEGER, username TEXT, password TEXT)''')

        conn.commit()
        conn.close()

    @staticmethod
    def add_user(username, password):
        conn, c = DbManager.connect_user_db()

        user_id = DbManager.get_id()
        hashed_password = DbManager.hash_password(password)

        values = [(user_id, username, hashed_password)]

        c.executemany('INSERT INTO users VALUES (?,?,?)', values)
        conn.commit()
        conn.close()

    @staticmethod
    def username_exists(username):
        conn, c = DbManager.connect_user_db()

        found = False
        for row in c.execute('''SELECT username FROM users'''):
            if row[0] == username:
                found = True

        conn.commit()
        conn.close()

        return found

    @staticmethod
    def get_id():
        conn, c = DbManager.connect_user_db()

        id_tuple = [value for value in c.execute('''SELECT COUNT(*) FROM users''')]

        conn.commit()
        conn.close()

        current_id = id_tuple[0][0]

        return current_id + 1

    @staticmethod
    def get_pwd(username):
        conn, c = DbManager.connect_user_db()

        pwd = list(c.execute('''SELECT password FROM users WHERE username = (?)''', [(username)]))[0][0]

        conn.commit()
        conn.close()

        return pwd

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(str.encode(password)).hexdigest()

    @staticmethod
    def confirm_password(password, confirm_password):
        if password != confirm_password:
            return False
        return True

    @staticmethod
    def check_password(password, hashed_pwd):
        if DbManager.hash_password(password) != hashed_pwd:
            return False
        return True

