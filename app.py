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
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
# Импорты связанные с Werkzeug 
from werkzeug.security import generate_password_hash, check_password_hash
# Импорты связанные с файлами проекта 
from FDataBase import FDataBase
from UserLogin import UserLogin

# Основной код поректа 

DATABASE = ('/tmp/flasksite2.db')
DEBUG = True
SECRET_KEY = os.getenv('SECRET_KEY')


app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flasksite2.db')))

# Инициализация LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

# Указываем, куда перенаправлять неавторизованных пользователей
login_manager.login_view = 'login'

# Функция загрузки пользователя по user_id
@login_manager.user_loader
def load_user(user_id):
    user = dbase.getUserId(user_id)
    if user:
        return UserLogin().create(user)
    return None

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


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = dbase.getUserByEmail(request.form['username'])
        if user and check_password_hash(user['hash_password'], request.form['password']):
            userLogin = UserLogin().create(user)
            login_user(userLogin)  # Авторизуем пользователя
            return redirect(url_for('index'))

        flash('Неверный логин или пароль', 'error')

    return render_template('login.html')


# Обработчик страницы регистрации
@app.route('/registration', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        if len(request.form['username']) < 4:
            flash('В usernamae должно быть больше символов', 'error')
            return render_template('registration.html')
        
        # Проверка username в базе данных 
        user_check = dbase.getUserUsername(request.form['username'])
        if user_check and user_check['count'] > 0: # Проверяем вернулся ли результат и count > 0
            flash('Пользователь с таким username уже существует', 'error')
            return render_template('registration.html')

        # Проверка на длину email
        if len(request.form['email']) < 4:
            flash('Ваш email должен быть более 4 символов', 'error')
            return render_template('registration.html')

        # Проверка есть ли email в базе данных
        email_check = dbase.getUserEmail(request.form['email'])
        if email_check and email_check['count'] > 0: # Проверяем вернулся ли результат и count > 0 
            flash('Пользователь с таким email уже существует', 'error')
            return render_template('registration.html')

        # Проверка длинны пароля 
        if len(request.form['password']) < 4 or request.form['password'] != request.form['confirm_password']:
            flash('Пароль не надежный, введите больше символов либо пароли не совпадают', 'error')
            return render_template('registration.html')

        # Если все верно 
        hash = generate_password_hash(request.form['password'])
        res = dbase.addUser(request.form['username'], request.form['email'], hash)
        if res:
            flash('Вы успешно зарегестрированы ! Пожалуйста войдите в систему')
            return redirect(url_for('login'))
                
    
    return render_template('registration.html')

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', username=current_user.username, enail=current_user.email)



@app.route('/finance', methods=['GET', 'POST'])
@login_required
def finance():
    user_id = current_user.get_id()
    old_balance = dbase.getBalance(user_id) or 0

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'update_balance':
            try:
                add_amount = float(request.form.get('add_balance', 0))
                if add_amount < 0:
                    flash('Сумма пополнения не может быть отрицательной.', 'error')
                else:
                    new_balance = old_balance + add_amount
                    if dbase.updateBalance(user_id, new_balance):
                        flash(f'Баланс успешно пополнен на {add_amount}.', 'success')
                    else:
                        flash('Ошибка при обновлении баланса.', 'error')
            except ValueError:
                flash('Введите корректное значение для пополнения баланса.', 'error')

        elif action == 'add_category':
            name = request.form.get('name', '').strip()
            color = request.form.get('color', '').strip()
            if not name:
                flash('Название категории не может быть пустым.', 'error')
            elif not color:
                flash('Цвет категории не указан.', 'error')
            else:
                if dbase.addCategory(user_id, name, color):
                    flash('Категория успешно добавлена.', 'success')
                else:
                    flash('Ошибка при добавлении категории.', 'error')

        elif action == 'add_expense':
            try:
                category_id = int(request.form.get('category_id'))
                name = request.form.get('expense_name', '').strip()
                amount = float(request.form.get('expense_amount', 0))

                if not name or amount <= 0:
                    flash('Введите корректные данные для траты.', 'error')
                else:
                    balance = dbase.getBalance(user_id) or 0
                    if amount > balance:
                        flash('Недостаточно средств на балансе для этой траты.', 'error')
                    else:
                        if dbase.addExpense(user_id, category_id, name, amount):
                            new_balance = balance - amount
                            dbase.updateBalance(user_id, new_balance)
                            flash('Трата успешно добавлена и баланс обновлён.', 'success')
                        else:
                            flash('Ошибка при добавлении траты.', 'error')
            except ValueError as e:
                flash(f'Некорректные данные: {e}', 'error')

        elif action == 'delete_category':
            try:
                category_id = int(request.form.get('category_id'))
                if dbase.deleteCategory(user_id, category_id):
                    flash('Категория успешно удалена.', 'success')
                else:
                    flash('Ошибка при удалении категории.', 'error')
            except ValueError:
                flash('Некорректный ID категории.', 'error')

        elif action == 'delete_expense':
            try:
                expense_id = int(request.form.get('expense_id'))
                expense = dbase.getExpenseById(user_id, expense_id)
                if expense:
                    amount = expense['amount']
                    if dbase.deleteExpense(user_id, expense_id):
                        balance = dbase.getBalance(user_id) or 0
                        dbase.updateBalance(user_id, balance + amount)
                        flash('Трата успешно удалена, баланс обновлён.', 'success')
                    else:
                        flash('Ошибка при удалении траты.', 'error')
                else:
                    flash('Трата не найдена.', 'error')
            except ValueError:
                flash('Некорректный ID траты.', 'error')

        return redirect(url_for('finance'))

    balance = dbase.getBalance(user_id) or 0
    categories = dbase.getCategoriesWithExpenses(user_id)
    total_expenses = sum(cat['total'] for cat in categories)

    return render_template(
        'finance.html',
        balance=balance,
        categories=categories,
        total_expenses=total_expenses
    )





            



@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы')
    return redirect(url_for('index'))







if __name__ == '__main__':
    app.run(debug=True)

