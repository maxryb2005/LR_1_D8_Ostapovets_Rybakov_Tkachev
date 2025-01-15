import sqlite3
import random
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes


# Функция для создания таблицы, если её нет
def create_table():
    conn = sqlite3.connect('jokes.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS jokes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        joke TEXT NOT NULL)''')
    conn.commit()
    conn.close()


# Функция для заполнения базы данных анекдотами (если таблица пустая)
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


# Главная функция
def main():
    # Создаем таблицу и заполняем анекдотами
    create_table()
    fill_jokes()

    # Токен бота
    token = '7885675764:AAGtWYFfFembmWYQ1lpHdvvtLSl3IOLScf4'

    # Создаем приложение для бота
    application = Application.builder().token(token).build()

    # Добавляем обработчик команды /joke
    application.add_handler(CommandHandler("joke", joke))

    # Запускаем бота
    application.run_polling()


if __name__ == '__main__':
    main()
