import sqlite3 as sql

fl = input("DB file ")

con = sql.connect(fl + ".db")
with con:
    cur = con.cursor()
    cur.execute("SELECT * FROM translates")
    rows = cur.fetchall()
    o = 0
    for row in rows:
        for g in row:
            print(g, end = ('- '))
        print()

    con.commit()
    cur.close()
