import telebot
import sys
sys.path.append("../")
from cfg.cfg import Config
from src.SQLite import SQLite
config = Config()
database_name = '../' + config.database_name
url = config.url

bot = telebot.TeleBot(config.token)

if __name__ == "__main__":
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
                else: pass
                print(f, user[0], row[0], chat[1])
            if not f:
                print(not f)
                sql.setChat(user[0], row[0])
                bot.send_message(user[0], row[1] + "\n\r" + row[3] + "\n\r"
                                 + url + "/" + row[0])
    sql.close()