import sqlite3
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes


# Функция для создания таблицы для анекдотов
def create_jokes_table():
    conn = sqlite3.connect('jokes.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS jokes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        joke TEXT NOT NULL)''')
    conn.commit()
    conn.close()


# Функция для создания таблицы для записи команд
def create_commands_table():
    conn = sqlite3.connect('commands.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS commands (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        command TEXT NOT NULL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()


# Функция для заполнения базы данных анекдотами
def fill_jokes():
    conn = sqlite3.connect('jokes.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM jokes")
    count = cursor.fetchone()[0]
    if count == 0:  # Если таблица пустая, добавляем анекдоты
        jokes = [
            "Почему программисты не могут идти в спортзал? Потому что они привыкли к 'состояниям'.",
            "Встретились два кота: один говорит: 'Я тебя люблю'. Другой: 'А я тебя ненавижу'. Первый: 'Ну, не переживай, это тоже любовь'.",
            "Как называют глупых людей в интернете? 'Пользователи'.",
            "Как стать успешным программистом? Нужно просто забыть об этом."
        ]
        for joke in jokes:
            cursor.execute("INSERT INTO jokes (joke) VALUES (?)", (joke,))
        conn.commit()
    conn.close()


# Функция для записи команды в базу данных
def log_command(command: str):
    conn = sqlite3.connect('commands.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO commands (command) VALUES (?)", (command,))
    conn.commit()
    conn.close()


# Функция для получения случайного анекдота из базы данных
def get_random_joke():
    conn = sqlite3.connect('jokes.db')
    cursor = conn.cursor()
    cursor.execute("SELECT joke FROM jokes ORDER BY RANDOM() LIMIT 1")
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else "Анекдоты закончились."


# Обработчик команды /joke
async def joke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    joke_text = get_random_joke()
    await update.message.reply_text(joke_text)


# Обработчик команды /help
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = "Этот бот предоставляет случайные анекдоты. Используйте команду /joke для получения анекдота."
    log_command("/help")  # Логируем команду /help
    await update.message.reply_text(help_text)


# Обработчик команды /about
async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    about_text = "Этот бот был создан для демонстрации работы с Telegram API и SQLite."
    log_command("/about")  # Логируем команду /about
    await update.message.reply_text(about_text)


# Главная функция
def main():
    # Создаем таблицы и заполняем анекдоты
    create_jokes_table()
    create_commands_table()
    fill_jokes()

    # Токен бота
    token = '7885675764:AAGtWYFfFembmWYQ1lpHdvvtLSl3IOLScf4'

    # Создаем приложение для бота
    application = Application.builder().token(token).build()

    # Добавляем обработчики команд
    application.add_handler(CommandHandler("joke", joke))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("about", about))

    # Запускаем бота
    application.run_polling()


if __name__ == '__main__':
    main()
