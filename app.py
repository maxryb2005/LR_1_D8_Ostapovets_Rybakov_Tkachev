import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)  # Изменено на __name__
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jokes.db'
app.config['SECRET_KEY'] = 'ORT_SuperStars'
db = SQLAlchemy(app)

def get_db_connection():
    conn = sqlite3.connect('jokes.db')
    conn.row_factory = sqlite3.Row  # Для доступа к столбцам как к атрибутам
    return conn

class Joke(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

users = {
    "Super_admin": {"password": "Darkelza", "role": "Super_admin"},
    "user": {"password": "student1372313", "role": "user"}
}

class User(UserMixin):
    def __init__(self, username):  # Исправлено на __init__
        self.id = username
        self.role = users[username]["role"]

@login_manager.user_loader
def load_user(username):
    if username in users:
        return User(username)
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in users and users[username]['password'] == password:
            user = User(username)
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Неправильное имя пользователя или пароль', 'danger')

    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', username=current_user.id)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/statistics', methods=['GET'])
@login_required
def statistics():
    if current_user.role != 'Super_admin':
        return '''
        <html>
            <body style="text-align: center; padding: 50px;">
                <h1 style="color: red; font-size: 36px;">Доступно только Супер администратору!</h1>
                <p style="font-size: 20px;">У вас нет необходимых прав для доступа к этой странице.</p>
            </body>
        </html>
        ''', 403

    conn = sqlite3.connect('commands.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM commands")
    data = cursor.fetchall()
    conn.close()
    return render_template('stat.html', commands=data)


@app.route('/satisfactory', methods=['GET', 'POST'])
@login_required
def satisfactory():
    if current_user.role != 'Super_admin':
        return '''
        <html>
            <body style="text-align: center; padding: 50px;">
                <h1 style="color: red; font-size: 36px;">Доступно только Супер администратору!</h1>
                <p style="font-size: 20px;">У вас нет необходимых прав для доступа к этой странице.</p>
            </body>
        </html>
        ''', 403
    conn = get_db_connection()
    cursor = conn.cursor()
    if request.method == 'POST':
        joke_content = request.form['joke']
        if joke_content:
            try:
                cursor.execute("INSERT INTO jokes (joke) VALUES (?)", (joke_content,))
                conn.commit()
            except Exception as e:
                print(f"Ошибка: {e}")

    # Получаем все шутки для отображения на странице
    jokes = conn.execute('SELECT * FROM jokes').fetchall()
    conn.close()
    return render_template('satisfactory.html', jokes=jokes)



@app.route('/delete_joke/<int:joke_id>', methods=['POST'])
@login_required
def delete_joke(joke_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM jokes WHERE id = ?", (joke_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('satisfactory'))

def init_db():
    with app.app_context():
        db.create_all()

if __name__ == "__main__":  # Исправлено на __name__
    init_db()
    app.run(debug=True)
