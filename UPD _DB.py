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


hgj = Translator()
sql.execute("SELECT * FROM translates")
rows = sql.fetchall()
o = 0
mx = 0
pp = 0
for j in rows:
    if pp:
        nh = hgj.translate(j[0], src = "ru").text.lower()
        sql1.execute("SELECT buryat FROM translates WHERE russian = ?", (j))
        if sql1.fetchone() != None:
            print(nh, j[0])
            sql1.execute(
                "INSERT INTO translates VALUES (?, ?, ?, ?)",
                (str(j[0]), str(j[1]), str(nh), int(1)))
            db1.commit()

        time.sleep(1)
    else:
        if j[0] == 'приползти':
            pp = 1


