import random
import sqlite3

db = sqlite3.connect("_DB.db")
sql1 = db.cursor()

sql1.execute("""CREATE TABLE IF NOT EXISTS tests(
    id TEXT,
    wrd TEXT
)""")


db.commit()


def gr():
    id = input()
    wrd = input()

    sql1.execute("SELECT * FROM tests WHERE id = ? and wrd = ?", (id, wrd))
    if sql1.fetchone() != None:
        print(
            """есть в вашем списке тестов"""
        )
    else:
        sql1.execute("""INSERT INTO tests VALUES (?, ?)""", (id, wrd))
        db.commit()


def test1():
    id = input()
    id = str(id)
    sql1.execute("""SELECT * FROM tests WHERE id = ?""", (id,))
    sql_dct = db.cursor()
    for i in sql1.fetchall():
        sql_dct.execute("""SELECT * FROM translates WHERE russian= ?""",
                        (i[1], ))
        f = sql_dct.fetchone()

        sql_dct.execute("SELECT * FROM translates")
        sm_W = []
        for i1 in sql_dct.fetchall():
            if i1[1][0] == f[1][0] and i1[1] != f[1]:
                sm_W += [[i1[0], i1[1], i1[2]]]

        rd = random.randint(0, len(sm_W) - 1)

        rd1 = random.randint(0, len(sm_W) - 1)
        while rd == rd1:
            rd1 = random.randint(0, len(sm_W) - 1)

        v = [f[1], sm_W[rd][1], sm_W[rd1][1]]
        print(i[1])
        random.shuffle(v)
        print(v)
        ans = input()

        if (f[1] != ans):
            print(f"неправильно правильный ответ - {f[1]}")
        else:
            print("правильно!")
        print(f"{sm_W[rd][1]} - {sm_W[rd][0]}")
        print(f"{sm_W[rd1][1]} - {sm_W[rd1][0]}")


test1()
