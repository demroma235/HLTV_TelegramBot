import sqlite3

from cfg.cfg import Config
from src.SQLite import SQLite


import telebot
import urllib.request

from bs4 import BeautifulSoup
config = Config()
bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=["start"])
def repeat_all_messages(message):
    bot.send_message(message.chat.id, 'Чтобы начать получать новости введите /get_news')


@bot.message_handler(commands=["status"])
def repeat_all_messages(message):
    bot.send_message(message.chat.id, 'Все хорошо. Бот работает.')


@bot.message_handler(commands=["get_news"])
def get_news(message):
    sql = SQLite(database_name)
    try:
        sql.set_user(message.chat.id)
        bot.send_message(message.chat.id,
                         'Теперь вы будете получать новости. ')
        send_news(message)
    except sqlite3.IntegrityError:
        bot.send_message(message.chat.id,
                         'Вы уже получаете новости.')


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
    database_name = config.database_name

    bot.polling(none_stop=True)

