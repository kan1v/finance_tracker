# Импорты связанные с os 
import os
# Импорты связанные с   sqlite3
import sqlite3
# Импорты связанные с Flask
from flask import Flask, abort, g, render_template, request, flash, redirect, url_for, session

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
    return render_template('index.html')

@app.route('/news')
def news():
    news_name, news_text, news_time = dbase.getNews()
    news_data = zip(news_name, news_text, news_time)
    print(news_data)
    return render_template('news.html', news_data=news_data)


# Обработчик страницыы авторизации 
@app.route('/login')
def login():
    return render_template('login.html')

# Обработчик страницы регистрации
@app.route('/registration', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        if len(request.form['username']) < 4:
            flash('В usernmae должно быть больше символов', 'error')
        elif request.form['username'] == dbase.getUSerUsername(request.form['username']):
            flash('Пользователь с таким username уже существует', 'error')
        elif len(request.form['email']) < 4:
            flash('Введие корректное значение', 'error')
        elif request.form['email'] == dbase.getUserEmail(request.form['email']):
            flash('Пользователь с таким email уже существует', 'error')
        elif len(request.form['password']) < 4:
            flash('Пароль должен быть более надежный', 'error')
        elif request.form['password'] != request.form['confirm_password']:
            flash('Пароли должны совпадать', 'error')
        else:
            hash = generate_password_hash(request.form['password'])
            res = dbase.addUser(request.form['username'], request.form['email'], hash)
            if res:
                flash('Вы успешно зарегестрированы', 'success')
                return(redirect(url_for('login')))
            else:
                flash('Ошибка при добавлении в БД', 'error')
    
    return render_template('registration.html')







if __name__ == '__main__':
    app.run(debug=True)

