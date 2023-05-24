from googletrans import Translator
import telebot
from telebot import types
import tokens
import sqlite3
from fuzzywuzzy import fuzz
import random

db = sqlite3.connect("_DB.db")
sql = db.cursor()
db.commit()
facts = open("facts.txt")
rFacts = ['']
for i in facts:
    rFacts += [i]

global userMd
userMd = {'0': 142}

def num_to_word(a):
    numb_names = [["", "нэгэн", "хоёр", "гурбан", "дүрбэн", "табан", "зургаан", "долоон", "найман", "юһэн"],
                  ["", "арбан", "хорин", "гушан", "душан",
                   "табин", "жаран", "далан", "наян", "ерэн"],
                  ]

    numb_suffixes = ["",
                     "",
                     " зуун",
                     " мянга",
                     "",
                     " зуун",
                     " миллион"]

    lst = [int(i) for i in list(a)]
    n = len(lst)
    ans = ""
    if n > 7:
        return "error404, число слишком большое (лимит чисел - 1-9999999)"
    for i in range(0, n):
        ans += ((numb_names[0 if (n - i - 1) % 3 != 1 else 1]
                 [lst[i]] + numb_suffixes[n - 1 - i]) if lst[i] else "") + " "
    ans = ans.rstrip()
    return ans


bot = telebot.TeleBot(tokens.telegramm)
while 1:
    # try:
        @bot.message_handler(commands=['start'])
        def welcome(message):

            # db = sqlite3.connect("translate.db")
            # sql = db.cursor()
            markup = types.ReplyKeyboardMarkup(resize_keyboard=1)
            key1 = types.KeyboardButton("Перевод слов")
            key2 = types.KeyboardButton("Я хочу потренироваться  ")
            key3 = types.KeyboardButton("факт о Бурятии")
            markup.add(key1, key2, key3)

            bot.send_message(message.chat.id, f"Привет *{message.from_user.first_name}*\nЯ бот который поможет тебе с бурятским языком.\n Выбери функцию которую хочешь чтобы я выполнил",
                             parse_mode='Markdown', reply_markup=markup)

        @bot.message_handler(content_types=['text'])
        def main(message):
            print(f"{message.text} от {message.chat.id}")
            global userMd
            global ff1, ff2, bug
            ff1, ff2, bug, ff3, train = userMd.get(message.chat.id, [0, -1, 0, 0, []])
            userMd[message.chat.id] = [ff1, ff2, bug, ff3, train]
            cid = message.chat.id
            db = sqlite3.connect("_DB.db")
            sql = db.cursor()

            if ff3:
                userMd[cid][3] = 0
                wlst = message.text.split()
                for i in wlst:
                    i = i.lower()
                    sql.execute(f"SELECT * FROM translates WHERE russian = '{i}'")
                    translate_w = sql.fetchone()
                    if translate_w == None:
                        userMd[message.chat.id][-1] = []
                        mrkUp = types.ReplyKeyboardMarkup(
                            resize_keyboard=1)
                        key1 = types.KeyboardButton("Перевод слов")
                        key2 = types.KeyboardButton("Я хочу потренироваться")
                        key3 = types.KeyboardButton("факт о Бурятии")
                        mrkUp.add(key1, key2, key3)
                        
                        bot.send_message(message.chat.id, f"слова {i} нет в моем словаре",  reply_markup=mrkUp)
                        return
                    userMd[message.chat.id][-1] += [(translate_w[1], translate_w[0])]
                
                random.shuffle(userMd[message.chat.id][-1])
                m = types.InlineKeyboardMarkup(
                    row_width=2)
                item1 = types.InlineKeyboardButton(
                    "скажи перевод", callback_data='?')
                m.add(item1)

                bot.send_message(
                    message.chat.id, userMd[message.chat.id][-1][-1], m)
                return

            if len(train) != 0:
                m = types.InlineKeyboardMarkup(
                    row_width=2)
                item1 = types.InlineKeyboardButton("скажи перевод", callback_data='?')
                m.add(item1)
                if message.text.lower() != train[-1][1]:
                    bot.send_message(
                        message.chat.id, 'неверно', reply_markup=m)
                else:
                    bot.send_message(
                        message.chat.id, 'верно!')
                    userMd[message.chat.id][-1].pop()
                    if (len(userMd[cid][-1]) == 0):
                        mr = types.ReplyKeyboardMarkup(resize_keyboard=1)
                        key1 = types.KeyboardButton("Перевод слов")
                        key2 = types.KeyboardButton("Я хочу потренироваться")
                        key3 = types.KeyboardButton("факт о Бурятии")
                        mr.add(key1, key2, key3)

                        bot.send_message(
                            message.chat.id, 'слова закончились. Хорошая работа!', mr)
                    else:
                        bot.send_message(
                            message.chat.id, userMd[cid][-1][-1][0])
                return




            if bug:
                mrkUp = types.ReplyKeyboardMarkup(
                                    resize_keyboard=1)
                key1 = types.KeyboardButton("Перевод слов")
                key2 = types.KeyboardButton("Я хочу потренироваться")
                key3 = types.KeyboardButton("факт о Бурятии")
                mrkUp.add(key1, key2, key3)

                bot.send_message(
                    message.chat.id, 'Понятно. Учту в следующий  раз', reply_markup=mrkUp)
                userMd[cid][2] = 0
                return 
            #? ПЕРЕВОД С БУРЯТСКОГО
            

            if ff2 != -1:
                if ff2 == 1:
                    #? поиск похожих слов
                    ww = str(message.text)
                    ww = ww.lower()
                    #
                    sql.execute("SELECT * FROM translates")
                    rows = sql.fetchall()
                    o = 0
                    mx = 0
                    for j in rows:
                        ratio = fuzz.token_sort_ratio(ww, j[1])
                        if ratio > mx:
                            mx = ratio
                            str1 = j[1]

                    #? вывод
                    if mx == 100:
                        sql.execute(f"SELECT * FROM translates WHERE buryat = '{ww}'")
                        translate_w= sql.fetchone()
                        ttcount = int(translate_w[3]) + 1
                        if (ttcount < 30):
                            ttcount += random.randint(30, 60) 

                        bot.send_message(
                            message.chat.id, str(f"*{translate_w[0]}*\nэто слово переводили - {ttcount} человек!"), parse_mode='Markdown')
                        sql.execute(
                            f"UPDATE translates SET used = {ttcount} WHERE buryat = '{ww}'")
                        db.commit()
                    elif mx >= 70:
                        sql.execute(
                            f"SELECT * FROM translates WHERE buryat = '{str1}'")
                        translate_w = sql.fetchone()
                        ttcount = int(translate_w[3]) + 1
                        if (ttcount < 30):
                            ttcount += random.randint(30, 60)

                        bot.send_message(
                            message.chat.id, str(f"*{translate_w[0]}* _(возможно вы имели ввиду {str1})_\nэто слово переводили - {ttcount} человек!"), parse_mode='Markdown')
                        sql.execute(
                            f"UPDATE translates SET used = {ttcount} WHERE buryat = '{str1}'")
                        db.commit()

                    else:
                        bot.send_message(
                            message.chat.id, 'К сожалению такого слова еще нет')
                    

                    #
                    userMd[cid][1] = -1

                #? ПЕРЕВОД С РУССКОГО
                elif ff2 == 2:

                    ww = str(message.text)
                    ww = ww.lower()
                    #? перевод чисел
                    try:
                        ww = int(ww)
                        bot.send_message(message.chat.id, num_to_word(str(ww)))

                    except:
                    
                    #? перевод слов 

                        #? поиск похожих слов

                        sql.execute("SELECT * FROM translates")
                        rows = sql.fetchall()
                        o = 0
                        mx = 0
                        for j in rows:
                            ratio = fuzz.token_sort_ratio(ww, j[0])
                            if ratio > mx:
                                mx = ratio
                                str1 = j[0]
                        #? вывод
                        
                        if mx == 100:
                            sql.execute(
                                f"SELECT * FROM translates WHERE russian = '{ww}'")
                            translate_w = sql.fetchone()
                            ttcount = int(translate_w[3]) + 1
                            if (ttcount < 30):
                                ttcount += random.randint(30, 60) 
                            bot.send_message(
                                message.chat.id, str(f"*{translate_w[1]}*\nэто слово переводили - {ttcount} человек!"), parse_mode='Markdown')
                            sql.execute(
                                f"UPDATE translates SET used = {ttcount} WHERE russian = '{ww}'")
                            db.commit()
                        elif mx >= 70:
                            sql.execute(
                                f"SELECT * FROM translates WHERE russian = '{str1}'")
                            translate_w = sql.fetchone()


                            ttcount = int(translate_w[3]) + 1
                            if (ttcount < 30):
                                ttcount += random.randint(30, 60)

                            bot.send_message(
                                message.chat.id, str(f"*{translate_w[1]}* _(возможно вы имели ввиду {str1})_\nэто слово переводили - {ttcount} человек!"), parse_mode='Markdown')
                            sql.execute(
                                f"UPDATE translates SET used = {ttcount} WHERE russian = '{str1}'")
                            db.commit()

                        else:
                            bot.send_message(
                                message.chat.id, 'К сожалению такого слова еще нет')

                    userMd[cid][1] = -1
                #? Перевод с нгл
                elif ff2 == 3:
                    ww = str(message.text)
                    ww = ww.lower()
                    #
                    sql.execute("SELECT * FROM translates")
                    rows = sql.fetchall()
                    o = 0
                    mx = 0
                    for j in rows:
                        ratio = fuzz.token_sort_ratio(ww, j[2])
                        if ratio > mx:
                            mx = ratio
                            str1 = j[2]

                    #? вывод
                    if mx == 100:
                        sql.execute(
                            f"SELECT * FROM translates WHERE english = '{ww}'")
                        translate_w = sql.fetchone()

                        ttcount = int(translate_w[3]) + 1
                        if (ttcount < 30):
                            ttcount += random.randint(30, 60)

                        bot.send_message(
                            message.chat.id, str(f"*{translate_w[1]}*\nthis word has been translated by - {ttcount} people!"), parse_mode='Markdown')
                        sql.execute(
                            f"UPDATE translates SET used = {ttcount} WHERE english = '{ww}'")
                        db.commit()
                    elif mx >= 70:
                        sql.execute(
                            f"SELECT * FROM translates WHERE english = '{str1}'")
                        translate_w = sql.fetchone()
                        ttcount = int(translate_w[3]) + 1
                        if (ttcount < 30):
                            ttcount += random.randint(30, 60)

                        bot.send_message(
                            message.chat.id, str(f"*{translate_w[1]}* _(maybe you mean {str1})_\nthis word has been translated by - {ttcount} people!"), parse_mode='Markdown')
                        sql.execute(
                            f"UPDATE translates SET used = {ttcount  } WHERE buryat = '{str1}'")
                        db.commit()

                    else:
                        bot.send_message(
                            message.chat.id, 'this word does not exit yet ')

                    #
                    userMd[cid][1] = -1


                markup = types.InlineKeyboardMarkup(row_width=2)
                item1 = types.InlineKeyboardButton("Да", callback_data='y')
                markup.add(item1, types.InlineKeyboardButton("ошибка в переводе", callback_data='!'))
                bot.send_message(
                    message.chat.id, 'Хотите перевести еще слова, или я неправильно перевел?', reply_markup= markup
                )

            if ff1 == True:
                #? ПРВЕРКА КАКОЙ ЯЗЫК ВЫБРАЛ ЧЕЛ
                if message.text == "bur>rus":
                    bot.send_message(
                        message.chat.id, 'ок теперь введи слово на бурятском и я его переведу! вот буквы которых нет на клавиатуре\nү\nһ\nө',
                        reply_markup=types.ReplyKeyboardRemove())
                    userMd[cid][1] = 1
                    userMd[cid][0] = False
                elif message.text == 'rus>bur':
                    bot.send_message(
                        message.chat.id, 'ок теперь введи на слово на русском или число и я его переведу!',
                        reply_markup=types.ReplyKeyboardRemove())
                    userMd[cid][1] = 2
                    userMd[cid][0] = False
                elif message.text == 'eng>bur':
                    bot.send_message(
                        message.chat.id, 'ок теперь введи на слово и я его переведу!',
                        reply_markup=types.ReplyKeyboardRemove())
                    userMd[cid][1] = 3
                    userMd[cid][0] = False

                else:
                    bot.send_message(
                        message.chat.id, "пожалуйста введи язык из нижних кнопок"
                    )
            #? ВЫБОР ЯЗЫКА

            if message.text == "Перевод слов":
                userMd[cid][0] = True

                markup = types.ReplyKeyboardMarkup(resize_keyboard=1)
                key1 = types.KeyboardButton('bur>rus')
                key2 = types.KeyboardButton('rus>bur')
                key3 = types.KeyboardButton('eng>bur')
                markup.add(key1, key2, key3)

                bot.send_message(
                    message.chat.id, 'Ок теперь выбери язык из кнопок с которого нужно переводить\n', reply_markup=markup)

            if message.text == "факт о Бурятии":
                m = types.ReplyKeyboardMarkup(resize_keyboard=1)
                key1 = types.KeyboardButton("Перевод слов")
                key2 = types.KeyboardButton("Я хочу потренироваться")
                key3 = types.KeyboardButton("факт о Бурятии")
                m.add(key1, key2, key3)

                bot.send_message(
                    message.chat.id, random.choice(rFacts), reply_markup=m)
             
            if message.text == "Я хочу потренироваться" :
                bot.send_message(
                    message.chat.id, 'ок введи русские слова через пробел')
                userMd[message.chat.id][3] = 1

        #? ПРОВЕРКА КАИЕ КНОПКИ ПОД ТЕКСТОМ НАЖЛ ПОЛЬЗОВАТЕЛЬ
        @bot.callback_query_handler(func=lambda call: True)
        def callback_inline(call):
            # db = sqlite3.connect("translate.db")
            # sql = db.cursor()
            
            if call.message:
                ci = call.message.chat.id
                global userMd
                global ff1, ff2, bug
                ff1, ff2, bug, ff3, train = userMd.get(call.message.chat.id, [0, -1, 0, 0, []])
                userMd[call.message.chat.id] = [ff1, ff2, bug, ff3, train]
            #? повтор перевода
                if call.data == 'y':
                    userMd[ci][0] = True

                    markup = types.ReplyKeyboardMarkup(resize_keyboard=1)
                    key1 = types.KeyboardButton('bur>rus')
                    key2 = types.KeyboardButton('rus>bur')
                    key3 = types.KeyboardButton('eng>bur')
                    markup.add(key1, key2, key3)

                    bot.send_message(
                        call.message.chat.id, 'Ок теперь выбери язык из кнопок с которого нужно переводить', reply_markup=markup)
                #? н повтор превода
                if call.data == 'n':
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          text="Ок выбери язык и напиши текст который переводить", reply_markup=None)
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=1)
                    key1 = types.KeyboardButton("Перевод слов")
                    key2 = types.KeyboardButton("Я хочу потренироваться")
                    key3 = types.KeyboardButton("факт о Бурятии")
                    markup.add(key1, key2, key3)

                    bot.send_message(
                        call.message.chat.id, f"Привет!\nЯ бот который поможет тебе с бурятским языком.\nВыбери функцию которую ты хочешь чтобы я выполнил", reply_markup=markup)
                
                if call.data == '!':
                    userMd[call.message.chat.id][2] = 1
                    bot.send_message(call.message.chat.id, 'ой! Напиши мне перевод этого слова,  в следующий раз я это учту!')
                if call.data == '?':
                    bot.send_message(
                        call.message.chat.id, train[-1][1])
                    userMd[ci][-1].pop()
                    if (len(userMd[ci][-1]) == 0):
                        mr = types.ReplyKeyboardMarkup(resize_keyboard=1)
                        key1 = types.KeyboardButton("Перевод слов")
                        key2 = types.KeyboardButton("Я хочу потренироваться")
                        key3 = types.KeyboardButton("факт о Бурятии")
                        mr.add(key1, key2, key3)

                        bot.send_message(
                            call.message.chat.id, 'слова закончились. Хорошая работа!', mr)
                    else:
                        m = types.InlineKeyboardMarkup(
                                    row_width=2)
                        item1 = types.InlineKeyboardButton(
                            "скажи перевод", callback_data='?')
                        m.add(item1)

                        bot.send_message(call.message.chat.id, userMd[ci][-1], m)





        bot.polling()
    # except:
    #     pass
