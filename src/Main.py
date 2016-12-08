import os
import sqlite3

from telebot import types

from cfg.cfg import Config
from src.SQLite import SQLite

import telebot
import urllib.request
from bs4 import BeautifulSoup
import sys

sys.path.append("../")
config = Config()

bot = telebot.TeleBot(config.token)

def get_played_mathes():
    pass

def get_following_matches():
    req = urllib.request.Request(
        config.url,
        data=None,
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        }
    )
    list_matches = []
    f = urllib.request.urlopen(req)
    soup = BeautifulSoup(f.read(), "html.parser")
    matchesItems = BeautifulSoup(str(soup.find_all('div', 'frontpageMatchBox')), "html.parser")
    # print(matchesItems.prettify())
    for matchesItem in matchesItems:
        if matchesItem == "[" or matchesItem == "]" or matchesItem == ", ":
            pass
        else:
            print("-=---------------------")
            # print(matchesItem)
            matches = matchesItem.findAll('div')
            if len(matches) == 7:
                # for match in matches:
                q = BeautifulSoup(str(matches[0]), "html.parser")
                teams = q.findAll('span', {"style": ""})
                match = [teams[0].string, teams[4].string, "live"]
                list_matches.append(match)
                print(teams[0].string, teams[4].string)
            elif len(matches) == 5:
                # for match in matches:
                q = BeautifulSoup(str(matches), "html.parser")
                teams = q.findAll('span', {"style": ""})
                time = q.findAll('div', {"style": "font-size: 12px;color:black;"})

                try:
                    match = [teams[0].string, teams[1].string, time[0].string]
                    list_matches.append(match)
                except IndexError:
                    pass
    return list_matches



def get_buttons():
    keyboard = types.InlineKeyboardMarkup()
    status = types.InlineKeyboardButton(text='Status', callback_data="status")
    get_following_matches = types.InlineKeyboardButton(text='Get a list of the following matches', callback_data="get_following_matches")
    get_played_matches = types.InlineKeyboardButton(text='get a list of matches played', callback_data="get_played_matches")
    keyboard.add(status)
    keyboard.add(get_following_matches)
    keyboard.add(get_played_matches)
    return keyboard


@bot.message_handler(commands=["start"])
def repeat_all_messages(message):
    bot.send_message(message.chat.id, 'Чтобы начать получать новости введите /get_news')


@bot.message_handler(commands=["get_news"])
def get_news(message):
    sql = SQLite(database_name)
    try:
        sql.set_user(message.chat.id)
        bot.send_message(message.chat.id,
                         'Теперь вы будете получать новости. ', reply_markup=get_buttons())
        send_news(message)
    except sqlite3.IntegrityError:
        bot.send_message(message.chat.id,
                         'Вы уже получаете новости.', reply_markup=get_buttons())


@bot.callback_query_handler(func=lambda call: True)
def call_status(call):
    if call.message:
        if call.data == "status":
            bot.send_message(call.message.chat.id, "Все хорошо, все работает.", reply_markup=get_buttons())

        if call.data == "get_following_matches":
            list_matches = get_following_matches()
            print(len(list_matches))
            if list_matches:
                for l in list_matches:
                    bot.send_message(call.message.chat.id, l[0] + " vs " + l[1] + "\n\r" + str(l[2]))
            bot.send_message(call.message.chat.id, "It's all", reply_markup=get_buttons())

        if call.data == "get_played_matches":
            # list_matches = get_matches()
            # print(len(list_matches))
            # if list_matches:
            #     for l in list_matches:
            #         bot.send_message(call.message.chat.id, l[0] + " vs " + l[1] + "\n\r" + str(l[2]))
            bot.send_message(call.message.chat.id, "It's all", reply_markup=get_buttons())


@bot.message_handler(commands=["send_news"])
def send_news(message):
    sql = SQLite(database_name)

    news = sql.getNews()
    users = sql.getUsers()

    news.reverse()
    f = False
    news = news[0:10]
    news.reverse()
    for user in users:
        chats = sql.getChats(user[0])
        for row in news:
            f = False
            for chat in chats:
                if row[0] == chat[1]:
                    f = True
                else:
                    pass
                print(f, user[0], row[0], chat[1])
            if not f:
                print(not f)
                sql.setChat(user[0], row[0])
                bot.send_message(user[0], row[1] + "\n\r" + row[3] + "\n\r"
                                 + url + "/" + row[0])
    sql.close()


@bot.message_handler(commands=["set_news"])
def set_news(message):
    req = urllib.request.Request(
        config.url,
        data=None,
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        }
    )

    f = urllib.request.urlopen(req)
    soup = BeautifulSoup(f.read(), "html.parser")
    newsItems = BeautifulSoup(str(soup.find_all('div', 'newsItem')), "html.parser")
    news = newsItems.findAll('a', {"href": True, "title": True})
    news.reverse()

    print("Запись начинается")

    sql = SQLite(database_name)
    for n in news:
        req = urllib.request.Request(
            url + n['href'],
            data=None,
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
            }
        )
        f = urllib.request.urlopen(req)
        soup = BeautifulSoup(f.read(), "html.parser")
        content = BeautifulSoup(str(soup.find('div', 'rNewsContent')), "html.parser")
        print(content)
        # sql.set_news(n['title'], "content", "", n['href'])

    sql.close()
    print("Запись завершена")


if __name__ == '__main__':
    print('Бот запущен')
    config = Config()
    url = config.url
    token = config.token
    database_name = "../" + config.database_name

    bot.polling(none_stop=True)
