import sqlite3


class SQLite:

    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def set_news(self, link, title, content, ru_content):
        with self.connection:
            return self.cursor.execute('INSERT INTO news '
                                       ' VALUES (?, ?, ?, ?)',
                                        (link, title, content, ru_content)).fetchall()


    def set_user(self, id):
        with self.connection:
            return self.cursor.execute('INSERT INTO user '
                                       ' VALUES (?, ?)',
                                        (id, 1)).fetchall()

    def getChats(self, user_id):
        with self.connection:
            return self.cursor.execute('SELECT * FROM chat_news WHERE user_id = ?', (user_id,)).fetchall()

    def getNews(self):
        with self.connection:
            return self.cursor.execute('SELECT * FROM news').fetchall()

    def getUsers(self):
        with self.connection:
            return self.cursor.execute('SELECT * FROM user').fetchall()

    def setChat(self, id, url):
        with self.connection:
            return self.cursor.execute('INSERT INTO chat_news '
                                       ' VALUES (?, ?)',
                                       (id, url)).fetchall()

    def select_all_news(self):
        """ Получаем все строки из news"""
        with self.connection:
            return self.cursor.execute('SELECT * FROM news').fetchall()

    def select_single(self, rownum):
        """ Получаем одну строку с номером rownum """
        with self.connection:
            return self.cursor.execute('SELECT * FROM music WHERE id = ?', (rownum,)).fetchall()[0]

    def count_rows(self):
        """ Считаем количество строк """
        with self.connection:
            result = self.cursor.execute('SELECT * FROM music').fetchall()
            return len(result)

    def close(self):
        """ Закрываем текущее соединение с БД """
        self.connection.close()