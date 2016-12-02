import json
import sqlite3
import urllib.request

import sys
sys.path.append("../")
from cfg.cfg import Config
from bs4 import BeautifulSoup
from src.SQLite import SQLite

config = Config()
url = config.url


database_name = '../' + config.database_name
if __name__ == "__main__":
    req = urllib.request.Request(
        url,
        data=None,
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        }
    )
    sql = SQLite(database_name)
    f = urllib.request.urlopen(req)
    soup = BeautifulSoup(f.read(), "html.parser")
    newsItems = BeautifulSoup(str(soup.find_all('div', 'newsItem')), "html.parser")
    news = newsItems.findAll('a', {"href": True, "title": True})
    news.reverse()
    for n in news:
        translate_api = "https://translate.yandex.net/api/v1.5/tr.json/translate?key=trnsl.1.1.20161129T192203Z.87143e3548376d6c.b2322ae9722994bee68188d16b1f5ae43389f2ea&text=" + \
                        n['title'] + "&lang=ru"
        f_translate = "{\"code\": 1}"
        try:
            f_translate = urllib.request.urlopen(translate_api).read().decode('utf-8')
        except UnicodeEncodeError:
            pass

        text_translate = json.loads(f_translate)
        if int(text_translate['code']) == 200:
            try:
                sql.set_news(str(n['href']), str(n['title']), "content", str(text_translate['text']))
            except sqlite3.IntegrityError:
                pass
        else:
            pass
