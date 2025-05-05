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


    def getUSerUsername(self, username):
        try:
            self.__cur.execute("SELECT username FROM  users WHERE username = ?", (username,))
            res = self.__cur.fetchone()
            if res:
                return res
        except sqlite3.Error as e:
            print(f'Ошибка при выполнееи запроса: {e}')
            return False
        
    def getUserEmail(self, email):
        try:
            self.__cur.execute("SELECT username FROM  users WHERE email = ?", (email,))
            res = self.__cur.fetchone()
            if res:
                return res
        except sqlite3.Error as e:
            print(f'Ошибка при выполнееи запроса: {e}')
            return False
        
    def addUser(self, username, email, hash_password):
        try:
            self.__cur.execute("INSERT INTO users VALUES(NULL, ?,?,?)", (username, email, hash_password))
            self.__db.commit()
            return True
        except sqlite3.Error as e:
            print(f'Ошибка доблавения пользователя в БД {e}')
            return False


