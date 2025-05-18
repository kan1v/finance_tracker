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
        
    # Получение баланса пользователя     
    def getBalance(self, user_id):
        try:
            # Выполняем запрос для получения баланса
            self.__cur.execute("SELECT amount FROM balances WHERE user_id = ?", (user_id,))
            row = self.__cur.fetchone()
            
            # Если запись не найдена, возвращаем 0
            if row is None:
                return 0
            
            # Проверяем и возвращаем значение баланса
            return row['amount'] if 'amount' in row.keys() else 0

        except sqlite3.Error as e:
            # Логируем ошибки, связанные с базой данных
            print(f"Ошибка базы данных при получении баланса: {e}")
            return 0

        except Exception as e:
            # Обработка других ошибок
            print(f"Неожиданная ошибка при получении баланса: {e}")
            return 0



    # Обновление баланса пользователя 
    def updateBalance(self, user_id, new_balance):
        try:
            self.__cur.execute(
                "INSERT INTO balances (user_id, amount) VALUES (?, ?) "
                "ON CONFLICT(user_id) DO UPDATE SET amount = excluded.amount",
                (user_id, new_balance)
            )
            self.__db.commit()
            return True
        except sqlite3.Error as e:
            print(f"Ошибка базы данных при обновлении баланса: {e}")
            return False

    # Добавление категории 
    def addCategory(self, user_id, name, color):  
        try:
            self.__cur.execute("INSERT INTO categories (user_id, name, color) VALUES (?, ?, ?)", 
                               (user_id, name, color))
            self.__db.commit()
            return True
        except sqlite3.Error as e:
            print(f"Ошибка добавления категории: {e}")
            return False

    # Получение категорий пользователя 
    def getCategories(self, user_id):      
        try:
            self.__cur.execute("SELECT * FROM categories WHERE user_id = ?", (user_id,))
            return self.__cur.fetchall()
        except sqlite3.Error as e:
            print(f"Ошибка получения категорий: {e}")
            return []

    # Добавление траты пользователя 
    def addExpense(self, user_id, category_id, name, amount):       
        try:
            self.__cur.execute("INSERT INTO expenses (user_id, category_id, name, amount) VALUES (?, ?, ?, ?)", 
                               (user_id, category_id, name, amount))
            self.__db.commit()
            return True
        except sqlite3.Error as e:
            print(f"Ошибка добавления траты: {e}")
            return False
        
    # Получение траты пользователя 
    def getExpenses(self, user_id):
        try:
            self.__cur.execute("""
                SELECT e.id, e.name, e.amount, e.date, c.name as category_name
                FROM expenses e
                JOIN categories c ON e.category_id = c.id
                WHERE e.user_id = ?
            """, (user_id,))
            return self.__cur.fetchall()
        except sqlite3.Error as e:
            print(f"Ошибка получения трат: {e}")
            return []
        
    def getCategoriesWithExpenses(self, user_id):
        self.__cur.execute(
            "SELECT id, name, color FROM categories WHERE user_id = ?", (user_id,)
        )
        categories = []
        rows = self.__cur.fetchall()
        for row in rows:
            cat = dict(row)  # конвертация в словарь
            self.__cur.execute(
                "SELECT id, name, amount FROM expenses WHERE category_id = ?", (cat['id'],)
            )
            expenses = self.__cur.fetchall()
            cat['expenses'] = [dict(exp) for exp in expenses]

            # Считаем total расходов по категории
            cat['total'] = sum(exp['amount'] for exp in cat['expenses'])

            categories.append(cat)
        return categories

    def deleteCategory(self, user_id, category_id):
        try:
            self.__cur.execute("DELETE FROM categories WHERE user_id = ? AND id = ?",(user_id, category_id))
            self.__db.commit()
            return True
        except sqlite3.Error as e:
            print(f"Ошибка удаления категории из БД: {e}")
            return False

    def getExpenseById(self, user_id, expense_id):
        try:
            self.__cur.execute("SELECT amount FROM expenses WHERE user_id = ? AND id = ?", (user_id, expense_id))
            return self.__cur.fetchone()
        except sqlite3.Error as e:
            print(f'Ошибка получения траты из БД: {e}')
            return False

    def deleteExpense(self, user_id, expense_id):
        try:
            self.__cur.execute("DELETE FROM expenses WHERE user_id = ? AND id = ?", (user_id, expense_id))
            self.__db.commit()
            return True
        except sqlite3.Error as e:
            print(f'Ошибка удаления траты из БД: {e}')
            return False
        
