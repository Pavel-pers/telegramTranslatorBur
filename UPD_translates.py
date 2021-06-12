from bs4 import BeautifulSoup
import requests
import sqlite3
import time

db = sqlite3.connect("translate.db")
sql = db.cursor()


sql.execute("""CREATE TABLE IF NOT EXISTS translates(
russian TEXT,
buryat TEXT,
used BIGINT
)
""")
db.commit()


# ПАРСИНГ ПЕРЕВОДА

url = "http://burlang.ru/site/russian-translate"
userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36"

rus_str = open('words.txt', 'r', encoding="utf-8")

for rus_name in rus_str:
    def main():
        global rus_name
        global url
        global userAgent
        global sql
        global db

        try:
            rus_name = rus_name.replace('\n', '')
            print(rus_name)
            headers = {
                "user-agent": userAgent,
                "accept": "*/*",
                "x-requested-with": "XMLHttpRequest"
            }

            parameters = {
                "russian_word": rus_name
            }

            html = (requests.get(url, headers=headers, params=parameters).text)
            soup = BeautifulSoup(html, 'html.parser')
            item = soup.find('li')
            bur_name = (str(item).replace('<li>', '').replace('</li>', ''))

            #СОХРАНЕНИЕ ПЕРЕВОДА В БД
            if bur_name != 'None':
                sql.execute("SELECT buryat FROM translates WHERE russian = ?", (rus_name, ))
                hg = sql.fetchone()
                if hg != None:
                    sql.execute("INSERT INTO translates VALUES (?, ?, ?)",
                                (str(rus_name), str(bur_name), int(0)))
                    db.commit()
            return
        except:
            time.sleep(10)
            main()
    # !что бы началась генерация нужно добавить сюда main()


# for ii in sql.execute("SELECT * FROM translates"):
#     print(ii)
