from bs4 import BeautifulSoup
import requests
import sqlite3
import time
from googletrans import Translator

db = sqlite3.connect("translate.db")
sql = db.cursor()
db1 = sqlite3.connect("_DB.db")
sql1 = db1.cursor()


sql1.execute("""CREATE TABLE IF NOT EXISTS translates(
russian TEXT,
buryat TEXT,
english TEXT,
used BIGINT
)
""")
db1.commit()



sql.execute(
    "SELECT * FROM translates")
rows = sql.fetchall()
o = 0
mx = 0
pp = 0
for j in rows:
    if pp:
        print(j[0])
        translator = Translator()
        tr_w = translator.translate(j[0], dest='en').text.lower()
        sql1.execute("INSERT INTO translates VALUES (?, ?, ?, ?)",
                    (str(j[0]), str(j[1]), str(tr_w),int(0)))
        db1.commit()
    else:
        if j[0] == 'комната': 
            pp = 1


