
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
# con = sqlite3.connect("tutorial.db")
# cur = con.cursor()
# # res = cur.execute("DROP DATABASE photos;")
# cur.execute("CREATE TABLE photos(file_name  , date, file_id, user_id)")
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
    # global count
    upload.count += 1
    print("called upload")
    file_name = f"img{upload.count}.jpg"
    print("file name ", file_name)
    print("message ", message, end='\n')
    userID = message.from_user.id
    fileID = message.photo[-1].file_id
    print('fileID =', fileID)
    file_info = bot.get_file(fileID)
    print('file.file_path =', file_info.file_path)
    downloaded_file = bot.download_file(file_info.file_path)

    con = sqlite3.connect("tutorial.db")
    cur = con.cursor()
    res = cur.execute("SELECT name FROM sqlite_master")
    print(res.fetchall())
    # if res.fetchone() is not None:
    #     print("existing table is ", res.fetchone())
    # else:
        # cur.execute("CREATE TABLE photos(file_name, date, file_id, user_id)")
    print("con ", con)
    print("cur ", cur)
    date_now = date.today()
    # with open(file_name, 'wb') as new_file:
    #     new_file.write(downloaded_file)
    #     if "/" in file_name:
    #         file_name = file_name.split("/")[1]
    cur.execute("""
                INSERT INTO photos VALUES (?, ?, ?, ?);
            """, (file_name, date_now, fileID, userID))
    cur.execute("SELECT * FROM photos")
    print("all content from table after insertion ", cur.fetchall())
    con.commit()


upload.count = 0


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
        print("res -------\n", res.fetchall())
        print("rowcount now ", res.rowcount)

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
    # m = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    # btn = types.KeyboardButton("buy smth")
    # m.add(btn)
    # bot.send_message(message.from_user.id, "test", reply_markup=m)
    # print(m.to_json())





@bot.message_handler(content_types=['text'])
def await_reply(message):
    print(message)
    con = sqlite3.connect("tutorial.db")
    cur = con.cursor()
    searched_file = message.text
    print("searched ile is ", searched_file)
    query = f"SELECT * FROM photos WHERE file_name is " + "'" + searched_file + "';"
    print("query ", query)
    res = cur.execute(query)
    print("res on query ", res.fetchall())
    print(res.rowcount)
    if res.rowcount == 0 or res.rowcount == -1:
        bot.send_message(message.chat.id, "Such file doesn't exist, please read the manual")
    else:
        bot.send_photo(message.chat.id, res.fetchone()[2])
    # print(res.fetchall())

def send_photo(chat_id, file_name):
    bot.send_photo(chat_id, file_name)

bot.polling(none_stop=True)
