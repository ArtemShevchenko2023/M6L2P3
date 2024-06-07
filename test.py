import telebot
import sqlite3
from config import *
bot = telebot.TeleBot(token)
conn = sqlite3.connect('projects.db', check_same_thread=False)
c = conn.cursor()
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет! Этот бот поможет вам хранить ваши личные проекты. Для помощи пропиши /help!')
@bot.message_handler(commands=['help'])
def start_message(message):
    bot.send_message(message.chat.id, 'Все команды бота:\n/start - приветствие\n/help - помощь по всем командам\n/add - добавить новую запись\n/show - все ваши записи\n/edit - редактирование описания записи\n/delete - удаление записи')
@bot.message_handler(commands=['add'])
def add_project(message):
    bot.send_message(message.chat.id, 'Введите название проекта:')
    bot.register_next_step_handler(message, add_description)
def add_description(message):
    global project_name
    project_name = message.text
    bot.send_message(message.chat.id, 'Введите описание проекта:')
    bot.register_next_step_handler(message, save_project)
def save_project(message):
    global project_name
    project_desc = message.text
    c.execute("INSERT INTO projects (name, description) VALUES (?, ?)", (project_name, project_desc))
    conn.commit()
    bot.send_message(message.chat.id, 'Проект успешно сохранен!')

@bot.message_handler(commands=['show'])
def showprojects(message):
    bot.send_message(message.chat.id, 'Вот ваши проекты:')
    projects = c.execute("SELECT name, description FROM Projects").fetchall()
    if projects:
        for project in projects:
            bot.send_message(message.chat.id, f'{project[0]}: {project[1]}')
    else:
        bot.send_message(message.chat.id, 'У вас пока нет сохраненных проектов.')
@bot.message_handler(commands=['delete'])
def deleteproject(message):
    bot.send_message(message.chat.id, 'Введите название проекта для удаления:')
    bot.register_next_step_handler(message, removeproject)
def removeproject(message):
    projectname = message.text
    c.execute("DELETE FROM Projects WHERE name = ?", (projectname,))
    conn.commit()
    bot.send_message(message.chat.id, 'Проект успешно удален!')
@bot.message_handler(commands=['edit'])
def editproject(message):
    bot.send_message(message.chat.id, 'Введите название проекта для редактирования:')
    bot.register_next_step_handler(message, editdescription)
def editdescription(message):
    global projectname
    projectname = message.text
    bot.send_message(message.chat.id, 'Введите новое описание проекта:')
    bot.register_next_step_handler(message, updateproject)
def updateproject(message):
    projectdesc = message.text
    c.execute("UPDATE Projects SET description = ? WHERE name = ?", (projectdesc, projectname))
    conn.commit()
    bot.send_message(message.chat.id, 'Проект успешно отредактирован!')
bot.polling()
conn.close()