import random

import telebot
import requests
from telebot import types
from telebot.types import ReplyKeyboardRemove
from translate import Translator


bot = telebot.TeleBot('6126019747:AAGDR8U4y3Be1PFPoYq3TEuKsYLGVplouB4')
API_KEY = "fad4160c96557a64eebd1739f664742d"
nasa_api_key = "N2q0SreNWk3ZGj0a0Mz3f7Q9tI4GyCQw1Rye6Lps"

translator = Translator(to_lang="ru")

# Клавиатура с командами в виде кнопок


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Я твой персональный помощник по задачам. Напиши /help, чтобы узнать, что я могу.")


#reply_markup=ReplyKeyboardRemove()

@bot.message_handler(commands=['help'])
def help(message):
    kb = types.InlineKeyboardMarkup(row_width=2)
    button1 = types.InlineKeyboardButton(text='Узнать погоду', callback_data="but1")
    button2 = types.InlineKeyboardButton(text='Фото космоса', callback_data="but2")
    kb.add(button1, button2)
    bot.send_message(message.chat.id, text="Мои функции", reply_markup=kb)

@bot.callback_query_handler(func=lambda callback: True)
def but_pressed(callback):
    help_message1 = '''Существующие функции:
    - /weather <город> - Получение информации о погоде в введеном городе
    '''
    help_message2 = '''Существующие функции:
    - /space_photo <YYYY-MM-DD> - Получение фотографии, сделанной NASA в введеную дату
    - /today_photo - Получении фотографии, сделанной NASA сегодня
    - /random_photo - Получение фотографии, сделанной NASA в рандомный день
    '''
    item0 = types.KeyboardButton("/help")
    if callback.data == "but1":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item = types.KeyboardButton("/weather")
        markup.add(item0, item)
        bot.send_message(callback.message.chat.id, help_message1, reply_markup=markup)
    elif callback.data == "but2":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("/space_photo")
        item2 = types.KeyboardButton("/today_photo")
        item3 = types.KeyboardButton("/random_photo")
        markup.add(item0, item1, item2, item3)
        bot.send_message(callback.message.chat.id, help_message2, reply_markup=markup)


# @bot.message_handler(commands=['weather'])
# def weather(message):
#     try:
#         city = message.text.split(" ")[1]
#         url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}'
#         response = requests.get(url)
#
#         if response.status_code == 200:
#             data = response.json()
#             temp_celsius = round(data['main']['temp'] - 273.15, 1)
#             weather_description = data['weather'][0]['description']
#             message_text = f'Текущая температура в {city.capitalize()}: {temp_celsius}°C.\n{translator.translate(weather_description).capitalize()}.'
#         else:
#             message_text = 'Неизвестный город. Попробуйте еще раз.'
#
#         bot.send_message(message.chat.id, message_text)
#
#     except Exception as e:
#         bot.send_message(message.chat.id, "Произошла ошибка. Проверьте правильность ввода команды. Требуется ввести город.")

user_states = {}

@bot.message_handler(commands=['weather'])
def weather(message):
    chat_id = message.chat.id

    # Проверяем, есть ли аргументы после команды /weather
    if len(message.text.split()) == 1:
        # Если нет аргументов, запрашиваем у пользователя город
        bot.send_message(chat_id, "Пожалуйста, укажите город.")
        # Устанавливаем состояние "ожидание города" для пользователя
        user_states[chat_id] = "waiting_for_city"
    else:
        city = " ".join(message.text.split(" ")[1:])
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}'
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            temp_celsius = round(data['main']['temp'] - 273.15, 1)
            weather_description = data['weather'][0]['description']
            message_text = f'Текущая температура в {city}: {temp_celsius}°C.\n{translator.translate(weather_description).capitalize()}.'
        else:
            message_text = 'Неизвестный город. Попробуйте еще раз.'

        bot.send_message(chat_id, message_text)

@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == "waiting_for_city")
def receive_city(message):
    chat_id = message.chat.id
    city = message.text

    # В этой функции мы ожидаем только название города
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        temp_celsius = round(data['main']['temp'] - 273.15, 1)
        weather_description = data['weather'][0]['description']
        message_text = f'Текущая температура в {city.capitalize()}: {temp_celsius}°C.\n{translator.translate(weather_description).capitalize()}.'
    else:
        message_text = 'Неизвестный город. Попробуйте еще раз.'

    bot.send_message(chat_id, message_text)

    # Снимаем состояние "ожидание города" для пользователя
    del user_states[chat_id]



# # Обработчик команды /space_photo
# @bot.message_handler(commands=['space_photo'])
# def send_space_photo(message):
#     try:
#         # Получаем дату из текста сообщения после команды
#         date = message.text.split(' ', 1)[1]
#
#         # Формируем URL для запроса к API NASA
#         url = f'https://api.nasa.gov/planetary/apod?api_key={nasa_api_key}&date={date}'
#
#         # Отправляем GET-запрос к API NASA
#         response = requests.get(url)
#
#         if response.status_code == 200:
#             data = response.json()
#             if data.get('media_type') == 'image':
#                 photo_url = data.get('url')
#                 title = data.get('title')
#                 # Отправляем фотографию пользователю
#                 bot.send_photo(message.chat.id, photo_url, caption=f'Фото, сделанное {date}:\n{translator.translate(title)}')
#             else:
#                 bot.send_message(message.chat.id, "На выбранную дату нет доступных фотографий космоса.")
#         else:
#             bot.send_message(message.chat.id, "Произошла ошибка при получении данных от API NASA.")
#
#     except Exception as e:
#         bot.send_message(message.chat.id, "Произошла ошибка. Проверьте правильность введенной даты. Нужно использовать формат YYYY-MM-DD")


@bot.message_handler(commands=['space_photo'])
def space_photo(message):
    chat_id = message.chat.id

    # Проверяем, есть ли аргументы после команды /space_photo
    if len(message.text.split()) == 1:
        # Если нет аргументов, запрашиваем у пользователя дату
        bot.send_message(chat_id, "Пожалуйста, укажите дату.")
        # Устанавливаем состояние "ожидание даты" для пользователя
        user_states[chat_id] = "waiting_for_date"
    else:
        date = message.text.split(' ', 1)[1]
        # Формируем URL для запроса к API NASA
        url = f'https://api.nasa.gov/planetary/apod?api_key={nasa_api_key}&date={date}'

        # Отправляем GET-запрос к API NASA
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            if data.get('media_type') == 'image':
                photo_url = data.get('url')
                title = data.get('title')
                # Отправляем фотографию пользователю
                bot.send_photo(message.chat.id, photo_url,
                               caption=f'Фото, сделанное {date}:\n{translator.translate(title)}')
            else:
                bot.send_message(message.chat.id, "На выбранную дату нет доступных фотографий космоса.")
        else:
            bot.send_message(message.chat.id, "Произошла ошибка при получении данных от API NASA.")

@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == "waiting_for_date")
def receive_city(message):
    chat_id = message.chat.id
    date = message.text

    # В этой функции мы ожидаем только название города
    url = f'https://api.nasa.gov/planetary/apod?api_key={nasa_api_key}&date={date}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data.get('media_type') == 'image':
            photo_url = data.get('url')
            title = data.get('title')
            # Отправляем фотографию пользователю
            bot.send_photo(message.chat.id, photo_url,
                           caption=f'Фото, сделанное {date}:\n{translator.translate(title)}')
        else:
            bot.send_message(message.chat.id, "На выбранную дату нет доступных фотографий космоса.")
    else:
        bot.send_message(message.chat.id, "Произошла ошибка при получении данных от API NASA.")


    # Снимаем состояние "ожидание города" для пользователя
    del user_states[chat_id]

@bot.message_handler(commands=['today_photo'])
def send_astronomy_picture(message):
    try:
        # Формируем URL для запроса к API NASA
        url = f'https://api.nasa.gov/planetary/apod?api_key={nasa_api_key}'

        # Отправляем GET-запрос к API NASA
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            if data.get('media_type') == 'image':
                photo_url = data.get('url')
                title = data.get('title')
                # Отправляем фотографию и описание пользователю
                bot.send_photo(message.chat.id, photo_url, caption=f'Фото, сделанное сегодня:\n{translator.translate(title)}')
            else:
                bot.send_message(message.chat.id, "Произошла ошибка при получении фотографии космоса.")
        else:
            bot.send_message(message.chat.id, "Произошла ошибка при получении данных от API NASA.")

    except Exception as e:
        bot.send_message(message.chat.id, "Произошла ошибка при получении данных от API NASA.")


def generate_random_date():
    # Генерируем случайный год в диапазоне от 2000 до 2023 (или другой нужный диапазон)
    year = random.randint(2000, 2023)

    # Генерируем случайный месяц в диапазоне от 1 до 12
    month = random.randint(1, 12)

    # Генерируем случайный день в зависимости от месяца
    if month in [1, 3, 5, 7, 8, 10, 12]:
        day = random.randint(1, 31)
    elif month == 2:
        # В феврале учитываем високосные годы
        if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
            day = random.randint(1, 29)
        else:
            day = random.randint(1, 28)
    else:
        day = random.randint(1, 30)

    # Форматируем дату в строку в формате "YYYY-MM-DD"
    date_str = f"{year}-{month:02d}-{day:02d}"

    return date_str

@bot.message_handler(commands=['random_photo'])
def send_random_space_photo(message):
    try:
        # Генерируем случайную дату
        random_date = generate_random_date()  # Замените на генерацию случайной даты
        url = f'https://api.nasa.gov/planetary/apod?api_key={nasa_api_key}&date={random_date}'

        # Отправляем GET-запрос к API NASA
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            if data.get('media_type') == 'image':
                photo_url = data.get('url')
                title = data.get('title')
                bot.send_photo(message.chat.id, photo_url, caption=f'Фото, сделанное {random_date}:\n{translator.translate(title)}')
            else:
                bot.send_message(message.chat.id, "Произошла ошибка при формировании даты. Попробуйте еще раз")
        else:
            bot.send_message(message.chat.id, "Произошла ошибка при получении данных от API NASA.")

    except Exception as e:
        bot.send_message(message.chat.id, "Произошла ошибка. Проверьте правильность введенной даты.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # Проверяем, является ли текст сообщения командой
    if message.text.startswith('/'):
        bot.send_message(message.chat.id, 'Команда не распознана. Попробуйте /help, чтобы узнать доступные команды.')
    else:
        bot.send_message(message.chat.id, 'Неопознанное сообщение. Попробуйте /help, чтобы узнать доступные команды.')


# # подключение к базе данных
# conn = sqlite3.connect('tasks.db', check_same_thread=False)
# cursor = conn.cursor()
#
# # создание таблицы задач
# cursor.execute('''CREATE TABLE IF NOT EXISTS tasks(id INTEGER PRIMARY KEY, user_id INTEGER, task TEXT, deadline TEXT, completed INTEGER)''')
# conn.commit()
#
# # функция для добавления задачи
# def add_task(user_id, task, deadline):
#     cursor.execute('INSERT INTO tasks (user_id, task, deadline, completed) VALUES (?, ?, ?, ?)',(user_id, task, deadline, 0))
#     conn.commit()
#
# # функция для удаления задачи
# def delete_task(task_id):
#     cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
#     for i in range (task_id + 1, cursor.execute('SELECT MAX(user_id) FROM tasks').fetchone()[0] - 1):
#         cursor.execute('SELECT * FROM tasks WHERE user_id = ?', i)
#     conn.commit()
#
# # функция для получения списка задач
# def get_tasks(user_id):
#     cursor.execute('SELECT * FROM tasks WHERE user_id = ?', (user_id,))
#     tasks = cursor.fetchall()
#     return tasks
#
# # функция для получения количества выполненных задач
# def get_completed_tasks(user_id):
#     cursor.execute('SELECT COUNT(*) FROM tasks WHERE user_id = ? AND completed = 1', (user_id,))
#     count = cursor.fetchone()[0]
#     return count
#
#
# # обработчик команды /new_task
# @bot.message_handler(commands=['new_task'])
# def new_task(message):
#     try:
#         task, deadline = message.text.split()[1:]
#         deadline = datetime.strptime(deadline, '%Y-%m-%d')
#         user_id = message.chat.id
#         add_task(user_id, task, deadline)
#         bot.reply_to(message, f'Задача "{task}" добавлена.')
#     except ValueError:
#         bot.reply_to(message, 'Неправильный формат даты. Используйте формат YYYY-MM-DD.')
#
# # обработчик команды /tasks
# @bot.message_handler(commands=['tasks'])
# def tasks(message):
#     user_id = message.chat.id
#     tasks = get_tasks(user_id)
#     if tasks:
#         tasks_list = '\n'.join(f'{task[0]}. {task[2]} ({task[3]}) {"[x]" if task[4] else ""}' for task in tasks)
#         bot.reply_to(message, f'Ваши задачи:\n{tasks_list}')
#     else:
#         bot.reply_to(message, 'У вас пока нет задач.')
#
# # обработчик команды /complete
# @bot.message_handler(commands=['complete'])
# def complete(message):
#     try:
#         task_id = int(message.text.split()[1])
#         user_id = message.chat.id
#         cursor.execute('UPDATE tasks SET completed = 1 WHERE id = ? AND user_id = ?', (task_id, user_id))
#         conn.commit()
#         bot.reply_to(message, f'Задача {task_id} отмечена как выполненная.')
#     except ValueError:
#         bot.reply_to(message, 'Неправильный номер задачи.')
#
# # обработчик команды /delete
# @bot.message_handler(commands=['delete'])
# def delete(message):
#     try:
#         task_id = int(message.text.split()[1])
#         user_id = message.chat.id
#         delete_task(task_id)
#         bot.reply_to(message, f'Задача {task_id} удалена.')
#
#     except ValueError:
#         bot.reply_to(message, 'Неправильный номер задачи.')
#
# # обработчик команды /stats
# @bot.message_handler(commands=['stats'])
# def stats(message):
#     user_id = message.chat.id
#     completed_tasks = get_completed_tasks(user_id)
#     total_tasks = len(get_tasks(user_id))
#     bot.reply_to(message, f'Выполнено задач: {completed_tasks}/{total_tasks}.')
#
# bot.polling()

bot.polling()