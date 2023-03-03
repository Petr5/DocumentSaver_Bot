
from os import getcwd

import telebot
from telebot import *
import json
import os
import sqlite3
from pydantic import BaseModel, ValidationError
import datetime
from datetime import date

TOKEN = "6017072825:AAF9WPDYwNQskOLrS1WUY6eVfKXIEW0HadU"
bot = telebot.TeleBot(TOKEN)
# bot.delete_webhook()

# print(getcwd())

# class photo

#
gcon = sqlite3.connect("tutorial.db")
gcur = gcon.cursor()
# # res = cur.execute("DROP DATABASE photos;")
# gcur.execute("CREATE TABLE photos(file_name  , date, file_id, user_id)")
# print(cur.fetchall())
@bot.message_handler(commands=['hello'])
def start(message):
    print("called start")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("👋 Поздороваться")
    markup.add(btn1)
    bot.send_message(message.from_user.id, "👋 Привет! Я твой бот-помошник!", reply_markup=markup)


@bot.message_handler(commands=['save'], content_types=['document', 'photo', 'audio', 'video', 'text'])
def save(message):
    bot.send_message(message.from_user.id, "save files working!")
    print("called save")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("👋 Обычный файл")
    markup.add(btn1)
    bot.send_message(message.from_user.id, "👋 Выбери категорию сохрняемого документа", reply_markup=markup)


@bot.message_handler(content_types=['document', 'photo', 'audio', 'video', 'voice']) # list relevant content types
def upload(message):
    upload.count += 1
    print("called upload")
    con = sqlite3.connect("tutorial.db")
    cur = con.cursor()
    file_name = f"img{upload.count}.jpg"
    print("file name ", file_name)
    print("message ", message, end='\n')
    user_id = message.from_user.id
    file_id = message.photo[-1].file_id
    print('fileID =', file_id)
    file_info = bot.get_file(file_id)
    print('file.file_path =', file_info.file_path)
    downloaded_file = bot.download_file(file_info.file_path)

    res = cur.execute("SELECT name FROM sqlite_master")
    print(res.fetchall())
    # if res.fetchone() is not None:
    #     print("existing table is ", res.fetchone())
    # else:
        # cur.execute("CREATE TABLE photos(file_name, date, file_id, user_id)")
    # print("con ", con)
    # print("cur ", cur)
    date_now = date.today()
    query = f"INSERT INTO photos (file_name, date, file_id, user_id) VALUES ('{file_name}', '{date_now}', '{file_id}', {user_id});"
    print("query which have doing to the database ", query)
    params = (file_name, date_now, file_id, user_id)
    cur.execute(query)
    cur.execute("SELECT * FROM photos")
    con.commit()
    print("all content from table after insertion ", cur.fetchall())

gcur.execute("select count(file_name) from photos")
# print("NUMBER OF ALL QUERIES IS ", cur.fetchall())
# print("NUMBER OF ALL QUERIES IS ", cur.fetchone()[0])
CNT_COLUMN_DB = gcur.fetchone()[0]
upload.count = CNT_COLUMN_DB


@bot.message_handler(commands=['chooseFile'], content_types=['text'])
def choose_photo(message):

    user_id = message.from_user.id
    print("user_id is ", user_id)
    print("called choose_file")

    directory = '.'
    reply = ""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    con = sqlite3.connect("tutorial.db")
    cur = con.cursor()
    cur.execute("SELECT name FROM sqlite_master")
    print("table is ", cur.fetchone())
    # if res.fetchone() is not None:
    #     print("existing table is ", res.fetchone())
    # else:
    #     cur.execute("CREATE TABLE photos(file_name, date, file_id, user_id)")

    con = sqlite3.connect("tutorial.db")
    cur = con.cursor()
    cur.execute(f"SELECT * FROM photos ")
    print("all db -------\n", cur.fetchall())
    print("rowcount now ", cur.rowcount)
    if (cur.rowcount != 0 ):
        res = cur.execute(f"SELECT * FROM photos where user_id is {user_id}")

        i = 0
        for row in res:
            print("i " + str(i) + " ", row)
            i += 1
            btn1 = types.KeyboardButton(row[0])
            markup.add(btn1)
        print("markup is ", markup.to_json())
        bot.send_message(message.from_user.id, "choose file from your store", reply_markup=markup)
    else:
        bot.send_message(message.from_user.id, "Now your store is empty, please send your photo in the chat")






@bot.message_handler(content_types=['text'])
def await_reply(message):
    print(message)
    con = sqlite3.connect("tutorial.db")
    cur = con.cursor()
    user_id = message.from_user.id
    searched_file = message.text
    print("searched ile is ", searched_file)
    if "select" in searched_file.lower() or "union" in searched_file.lower() or "where" in searched_file.lower() or "delete" in searched_file.lower() or "sqlite" in searched_file.lower()\
        or "from" in searched_file.lower() or "insert" in searched_file.lower():

        bot.send_message(message.chat.id, "Do not do things like that any more!!!!")
        print("HAHAH попался")
    else:
        query = f"SELECT * FROM photos WHERE file_name is '{searched_file}'  and user_id is {user_id};"
        print("query that have benn doing to database from ", query)
        res = cur.execute(query)

        result_on_user_query = res.fetchone()
        print("result_on_user_query ", result_on_user_query)
        if result_on_user_query is None:
            bot.send_message(message.chat.id, "Such file doesn't exist, please read the manual")
        else:
            bot.send_photo(message.chat.id, result_on_user_query[2])

def send_photo(chat_id, file_name):
    bot.send_photo(chat_id, file_name)

bot.polling(none_stop=True)
