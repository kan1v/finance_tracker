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
        sql = '''SELECT * FROM news'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res: return res
        except sqlite3.Error as e:
            print(f'Ошибка чтения из бд: {e}')

    def addNews(self, name, text):
        pass
