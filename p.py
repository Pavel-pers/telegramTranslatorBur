import sqlite3 as sql

con = sql.connect('translate.db')
with con:
    cur = con.cursor()
    cur.execute("SELECT * FROM translates")
    rows = cur.fetchall()
    o = 0
    for row in rows:
        if(row[0] == "ящур"):
            o = 1

    con.commit()
    cur.close()
