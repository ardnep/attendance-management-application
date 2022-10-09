import py7zr
import shutil
import os

from database import DbManager


class User:
    current_user = None
    current_user_password = None

    @staticmethod
    def init_new_user(username, password, confirm_password):
        DbManager.check_db()

        if username.strip() == '':
            return 'Invalid Username'

        if ' ' in username:
            return 'Username cannot contain spaces!'

        if password.strip() == '':
            return 'Invalid Password'

        if DbManager.username_exists(username):
            return 'Username already exists!'

        if not DbManager.confirm_password(password, confirm_password):
            return 'Passwords do not match!'

        DbManager.add_user(username, password)

        User.new_user_dir(username, password)

        return 'Successful!'

    @staticmethod
    def auth_user(username, password):
        DbManager.check_db()

        if username.strip() == '':
            return 'Invalid Username'

        if password.strip() == '':
            return 'Invalid Password'

        if not DbManager.username_exists(username):
            return "Username Doesn't Exist"

        hashed_pwd = DbManager.get_pwd(username)

        if DbManager.check_password(password, hashed_pwd):
            return 'Authorized'

        return 'Username or Password is Invalid'

    @staticmethod
    def set_current_user(username, password):
        User.current_user = username
        User.current_user_password = password

        with py7zr.SevenZipFile(f'users/{User.current_user}.7z', 'r', password=f'{User.current_user_password}') as user_dir:
            user_dir.extract()

        os.remove(f'users/{User.current_user}.7z')

    @staticmethod
    def user_logout():
        with py7zr.SevenZipFile(f'users/{User.current_user}.7z', 'w', password=f'{User.current_user_password}') as user_dir:
            user_dir.writeall(f'users/{User.current_user}')
        shutil.rmtree(f'users/{User.current_user}')
        User.current_user = None

    @staticmethod
    def new_user_dir(username, password):
        dir_name = f'users/{username}'
        os.makedirs(dir_name)

        with py7zr.SevenZipFile(f'users/{username}.7z', 'w', password=f'{password}') as user_dir:
            user_dir.writeall(f'users/{username}')

        shutil.rmtree(dir_name)
