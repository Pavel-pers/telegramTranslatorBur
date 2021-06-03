from googletrans import Translator
import telebot
from telebot import types
import bot_tokens
import sqlite3
from fuzzywuzzy import fuzz

db = sqlite3.connect("_DB.db")
sql = db.cursor()
db.commit()

ff1 = False
ff2 = -1
ff3 = False
stop = False


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


bot = telebot.TeleBot(bot_tokens.telegramm)

while 1:
    # try:
        @bot.message_handler(commands=['start'])
        def welcome(message):

            # db = sqlite3.connect("translate.db")
            # sql = db.cursor()
            markup = types.ReplyKeyboardMarkup(resize_keyboard=1)
            key1 = types.KeyboardButton("Перевод слов")
            key2 = types.KeyboardButton("Я хочу потренероватся")
            key3 = types.KeyboardButton("Рандомный факт о Бурятии")
            markup.add(key1, key2, key3)

            bot.send_message(message.chat.id, f"Привет *{message.from_user.first_name}*\nЯ бот который поможет тебе с бурятским языком.\nВыбери функцию которую ты хочешь что бы я выполнил",
                             parse_mode='Markdown', reply_markup=markup)

        @bot.message_handler(content_types=['text'])
        def main(message):
            global ff1
            global ff2
            db = sqlite3.connect("_DB.db")
            sql = db.cursor()

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
                        sql.execute(
                            f"SELECT * FROM translates WHERE buryat = '{ww}'")
                        translate_w = sql.fetchone()
                        bot.send_message(
                            message.chat.id, str(f"*{translate_w[0]}*\nэто слово переводили - {translate_w[3]} человек!"), parse_mode='Markdown')
                        r23 = translate_w[2] + 1
                        sql.execute(
                            f"UPDATE translates SET used = {r23} WHERE buryat = '{ww}'")
                        db.commit()
                    elif mx >= 70:
                        sql.execute(
                            f"SELECT * FROM translates WHERE buryat = '{str1}'")
                        translate_w = sql.fetchone()
                        bot.send_message(
                            message.chat.id, str(f"*{translate_w[0]}* _(возможно вы имели ввиду {str1})_\nэто слово переводили - {translate_w[3]} человек!"), parse_mode='Markdown')
                        r23 = translate_w[2] + 1
                        sql.execute(
                            f"UPDATE translates SET used = {r23} WHERE buryat = '{str1}'")
                        db.commit()

                    else:
                        bot.send_message(
                            message.chat.id, 'К сожалению такого слова еще нет ):')

                    #
                    ff2 = -1

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

                        print("1\n1\n1\n1\n1\n1\n1\n1\n")
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
                            bot.send_message(
                                message.chat.id, str(f"*{translate_w[1]}*\nэто слово переводили - {translate_w[3]} человек!"), parse_mode='Markdown')
                            r23 = translate_w[2] + 1
                            sql.execute(
                                f"UPDATE translates SET used = {r23} WHERE russian = '{ww}'")
                            db.commit()
                        elif mx >= 70:
                            sql.execute(
                                f"SELECT * FROM translates WHERE russian = '{str1}'")
                            translate_w = sql.fetchone()
                            bot.send_message(
                                message.chat.id, str(f"*{translate_w[1]}* _(возможно вы имели ввиду {str1})_\nэто слово переводили - {translate_w[3]} человек!"), parse_mode='Markdown')
                            r23 = translate_w[2] + 1
                            sql.execute(
                                f"UPDATE translates SET used = {r23} WHERE russian = '{str1}'")
                            db.commit()

                        else:
                            bot.send_message(
                                message.chat.id, 'К сожалению такого слова еще нет ):')

                    ff2 = -1
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
                        print(translate_w)
                        bot.send_message(
                            message.chat.id, str(f"*{translate_w[1]}*\nэто слово переводили - {translate_w[3]} человек!"), parse_mode='Markdown')
                        r23 = translate_w[3] + 1
                        sql.execute(
                            f"UPDATE translates SET used = {r23} WHERE english = '{ww}'")
                        db.commit()
                    elif mx >= 70:
                        sql.execute(
                            f"SELECT * FROM translates WHERE english = '{str1}'")
                        translate_w = sql.fetchone()
                        bot.send_message(
                            message.chat.id, str(f"*{translate_w[1]}* _(возможно вы имели ввиду {str1})_\nэто слово переводили - {translate_w[3]} человек!"), parse_mode='Markdown')
                        r23 = translate_w[3] + 1
                        sql.execute(
                            f"UPDATE translates SET used = {r23} WHERE buryat = '{str1}'")
                        db.commit()

                    else:
                        bot.send_message(
                            message.chat.id, 'К сожалению такого слова еще нет ):')

                    #
                    ff2 = -1


                markup = types.InlineKeyboardMarkup(row_width=2)
                item1 = types.InlineKeyboardButton("Да", callback_data='y')
                item2 = types.InlineKeyboardButton("Нет", callback_data='n')

                markup.add(item1, item2)

                bot.send_message(
                    message.chat.id, 'Вы хотите перевести еще слова?', reply_markup=markup
                )

            if ff1 == True:
                #? ПРВЕРКА КАКОЙ ЯЗЫК ВЫБРАЛ ЧЕЛ
                if message.text == "Бурятский":
                    bot.send_message(
                        message.chat.id, 'ок теперь введи слово на бурятском и я его переведу! вот буквы которых нет на клавиатуре\nү\nһ\nө',
                        reply_markup=types.ReplyKeyboardRemove())
                    ff2 = 1
                    ff1 = False
                elif message.text == 'Русский':
                    bot.send_message(
                        message.chat.id, 'ок теперь введи на слово на русском или число и я его переведу!',
                        reply_markup=types.ReplyKeyboardRemove())
                    ff2 = 2
                    ff1 = False
                elif message.text == 'Английский':
                    bot.send_message(
                        message.chat.id, 'ок теперь введи на слово и я его переведу!',
                        reply_markup=types.ReplyKeyboardRemove())
                    ff2 = 3
                    ff1 = False

                else:
                    bot.send_message(
                        message.chat.id, "пожалуйста введи язык из нижних кнопок"
                    )
            #? ВЫБОР ЯЗЫКА

            if message.text == "Перевод слов":
                ff1 = True

                markup = types.ReplyKeyboardMarkup(resize_keyboard=1)
                key1 = types.KeyboardButton('Бурятский')
                key2 = types.KeyboardButton('Русский')
                key3 = types.KeyboardButton('Английский')
                markup.add(key1, key2, key3)

                bot.send_message(
                    message.chat.id, 'Ок теперь выбери язык из кнопок с которого нужно переводить\n (свой язык - я автоматически определю язык)', reply_markup=markup)

            if message.text == "Рандомный факт о Бурятии":
                # ?НУ ТУТ НАДО БРАТЬ ФАКТЫ ИЗ БУРЯТИИ ИЗ БД НО ПОКА ЧТО Я ДРУГИМ ЗАНЯТ
                pass
            if message.text == "Я хочу потренироваться":
                # ?В НОВОМ АПДЕЙТЕ
                pass

        #? ПРОВЕРКА КАИЕ КНОПКИ ПОД ТЕКСТОМ НАЖЛ ПОЛЬЗОВАТЕЛЬ
        @bot.callback_query_handler(func=lambda call: True)
        def callback_inline(call):
            # db = sqlite3.connect("translate.db")
            # sql = db.cursor()
            
            if call.message:
                
                #? повтор перевода
                if call.data == 'y':
                    global ff1
                    ff1 = True

                    markup = types.ReplyKeyboardMarkup(resize_keyboard=1)
                    key1 = types.KeyboardButton('Бурятский')
                    key2 = types.KeyboardButton('Русский')
                    key3 = types.KeyboardButton('Английский')
                    markup.add(key1, key2, key3)

                    bot.send_message(
                        call.message.chat.id, 'Ок теперь выбери язык из кнопок с которого нужно переводить\n (свой язык - я автоматически определю язык) ', reply_markup=markup)
                #? н повтор превода
                if call.data == 'n':
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          text="Ок выбери язык и напиши текст который переводить", reply_markup=None)
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=1)
                    key1 = types.KeyboardButton("Перевод слов")
                    key2 = types.KeyboardButton("Я хочу потренероватся")
                    key3 = types.KeyboardButton("Рандомный факт о Бурятии")
                    markup.add(key1, key2, key3)

                    bot.send_message(
                        call.message.chat.id, f"Привет!\nЯ бот который поможет тебе с бурятским языком.\nВыбери функцию которую ты хочешь что бы я выполнил", reply_markup=markup)

        bot.polling()
    # except:
    #     pass
