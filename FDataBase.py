# Импорты для работы с файлом 
import math
import sqlite3
import time

# Основной код файла 

class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def getNews(self):
        try:
            self.__cur.execute("SELECT news_name, news_text, time FROM news")
            results = self.__cur.fetchall()  # Получаем все записи
            if results:
                # Распределяем данные по переменным
                news_name = [row[0] for row in results]
                news_text = [row[1] for row in results]
                news_time = [row[2] for row in results]
                return news_name, news_text, news_time
            else:
                return [], [], []  # Если данных нет, возвращаем пустые списки
        except sqlite3.Error as e:
            print(f'Ошибка чтения из БД: {e}')
            return [], [], []  # Если произошла ошибка, возвращаем пустые списки


    def getUserUsername(self, username):
        try:
            self.__cur.execute(f"SELECT COUNT() as 'count' FROM users WHERE username LIKE ?", (username,))
            res = self.__cur.fetchone()
            if res['count'] > 0:
                return res
        except sqlite3.Error as e:
            print(f'Ошибка проверки по username пользователя в БД: {e}')

        
    def getUserEmail(self, email):
        try:
            self.__cur.execute(f"SELECT COUNT() as 'count' FROM users WHERE email LIKE ?", (email,))
            res = self.__cur.fetchone()
            if res['count'] > 0:
                return res
        except sqlite3.Error as e:
            print(f'Ошибка проверки по email пользователя в БД: {e}')
        
    def addUser(self, username, email, hash_password):
        try:
            self.__cur.execute("INSERT INTO users VALUES(NULL, ?,?,?)", (username, email, hash_password))
            self.__db.commit()
            return True
        except sqlite3.Error as e:
            print(f'Ошибка доблавения пользователя в БД {e}')
            return False

    def getUserByEmail(self, username):
        try:
            self.__cur.execute("SELECT * FROM users WHERE username = ? LIMIT 1", (username,))
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False

            return res
        except sqlite3.Error as e:
            print(f"Ошибка получения данных из БД: {e}")

        return False
    
    def getUserId(self, user_id):
        try: 
            self.__cur.execute("SELECT * FROM users WHERE id = ? LIMIT 1", (user_id, ))
            res = self.__cur.fetchone()
            return res
        except sqlite3.Error as e:
            print(f"Не найден пользоваетль по ID: {e}")
            return None


