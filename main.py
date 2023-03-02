
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


# class Message(BaseModel):
#     file_id: str
#     file_unique_id: str
#     width: int
#     height: int
#     duration: int
#     # thumb: telebot.types.PhotoSize
#     file_name: str
#     mime_type: str
#     file_size: int


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
    # try:
    #     msg = Message.parse_raw(message)
    # except ValidationError as e:
    #     print("error ", e.json())

    # print ('message.photo =', message.photo)
    userID = message.from_user.id
    fileID = message.photo[-1].file_id
    # print('fileID =', fileID)
    file_info = bot.get_file(fileID)
    # print('file.file_path =', file_info.file_path)
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
    res = cur.execute("SELECT * FROM photos")
    print("all content from table are ", res.fetchall())
    date_now = date.today()
    with open(file_name, 'wb') as new_file:
        new_file.write(downloaded_file)
        if "/" in file_name:
            file_name = file_name.split("/")[1]
        cur.execute("""
                    INSERT INTO photos VALUES (?, ?, ?, ?);
                """, (file_name, date_now, fileID, userID))
        con.commit()


upload.count = 0


@bot.message_handler(commands=['chooseFile'], content_types=['text'])
def choose_photo(message):
    print("called choose_file")
    directory = '.'
    reply = ""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            if "/" in f:
                f = f.split("/")[1]
            print(f)
            reply += f"Файл: {f}\n"
            btn1 = types.KeyboardButton(f)
            markup.add(btn1)
    # print(reply)
    bot.send_message(message.from_user.id, reply, reply_markup=markup)

    # bot.send_photo(message.from_user.id, "img.jpg")
    # send_photo(message.from_user.id, "img.png")



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
    bot.send_photo(message.chat.id, res.fetchone()[2])
    # print(res.fetchall())

def send_photo(chat_id, file_name):
    bot.send_photo(chat_id, file_name)

bot.polling(none_stop=True)
