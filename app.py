# Импорты связанные с os 
import os
# Импорты связанные с   sqlite3
import sqlite3
# Импорты связанные с Flask
from flask import Flask, abort, g, render_template, request, flash, redirect, url_for

# Импоты связанные с python-dotenv
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())
# Импорты связанные с Flask-Login
from flask_login import LoginManager, login_user, login_required
# Импорты связанные с Werkzeug 
from werkzeug.security import generate_password_hash, check_password_hash
# Импорты связанные с файлами проекта 
from FDataBase import FDataBase

# Основной код поректа 

DATABASE = ('/tmp/flasksite2.db')
DEBUG = True
SECRET_KEY = os.getenv('SECRET_KEY')


app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flasksite2.db')))

# Подключение к базе данных 
def connect_db():
    connection = sqlite3.connect(app.config['DATABASE'])
    connection.row_factory = sqlite3.Row
    return connection

# Создание базы данных
def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())

    db.commit()
    db.close()

# Соеденение с базой данных если оно еще не было создано
def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()

    return g.link_db 

dbase = None
@app.before_request
def before_request():
    '''Установление соеденения с БД перед выполнением запроса'''
    global dbase
    db = get_db()
    dbase = FDataBase(db)



@app.teardown_appcontext
def close_db(error):
    '''Закрываем соеденения с БД если оно было установлено'''
    if hasattr(g, 'link_db'):
        g.link_db.close()

# Обработчик главной страницы и так же новостей 
@app.route('/')
def index():
    news_all_info = dbase.getNews()
    return render_template('index.html')










if __name__ == '__main__':
    app.run(debug=True)

