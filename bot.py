import telebot
import requests

bot = telebot.TeleBot('6126019747:AAGDR8U4y3Be1PFPoYq3TEuKsYLGVplouB4')
API_KEY = "fad4160c96557a64eebd1739f664742d"

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Привет! Я твой персональный помощник по задачам. Напиши /help, чтобы узнать, что я могу.')

@bot.message_handler(commands=['help'])
def help(message):
    help_message = '''Я умею делать следующее:
    #     - /weather <название города>'''
    bot.reply_to(message, help_message)


@bot.message_handler(commands=['weather'])
def weather(message):
    city = message.text.split(" ")[1]
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        temp_celsius = round(data['main']['temp'] - 273.15, 1)
        weather_description = data['weather'][0]['description']
        message_text = f'Current temperature in {city}: {temp_celsius}°C.\n{weather_description}.'
    else:
        message_text = 'Error. Try again.'

    bot.send_message(message.chat.id, message_text)

bot.polling()


# import telebot
# import sqlite3
# from datetime import datetime, date
#
# # токен бота
# bot = telebot.TeleBot('6126019747:AAGDR8U4y3Be1PFPoYq3TEuKsYLGVplouB4')
#
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
# # обработчик команды /start
# @bot.message_handler(commands=['start'])
# def send_welcome(message):
#     bot.reply_to(message, 'Привет! Я твой персональный помощник по задачам. Напиши /help, чтобы узнать, что я могу.')
#
# # обработчик команды /help
# @bot.message_handler(commands=['help'])
# def send_help(message):
#     help_message = '''Я умею делать следующее:
#     - /new_task <название задачи> <дата выполнения> - добавить новую задачу;
#     - /tasks - показать список задач;
#     - /complete <номер задачи> - отметить задачу как выполненную;
#     - /delete <номер задачи> - удалить задачу;
#     - /stats - показать статистику выполнения задач.'''
#     bot.reply_to(message, help_message)
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
# # запуск бота
# bot.polling()