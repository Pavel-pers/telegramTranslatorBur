import telebot
from telebot import types
import bot_tokens
import sqlite3

db = sqlite3.connect("translate.db")
sql = db.cursor()
db.commit()

ff1 = False
ff2 = -1
ff3 = False
stop = False
# try:


bot = telebot.TeleBot(bot_tokens.telegramm)

while 1:
    try:
        @bot.message_handler(commands = ['start'])
        def welcome(message):


            db = sqlite3.connect("translate.db")
            sql = db.cursor()
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
            db = sqlite3.connect("translate.db")
            sql = db.cursor()

            if ff2 != -1:
                if ff2 == 1:
                    ww = str(message.text)
                    ww = ww.lower()
                    
                    sql.execute(
                        f"SELECT * FROM translates WHERE buryat = '{ww}'")
                    translate_w = sql.fetchone()

                    if translate_w is None:
                        bot.send_message(
                            message.chat.id, 'К сожалению такого слова еще нет ):')
                    else:
                        bot.send_message(
                            message.chat.id, str(translate_w[0] + "\nэто слово переводили - " + str(translate_w[2]) + " человек!"))
                        r23 = translate_w[2] + 1
                        sql.execute(
                            f"UPDATE translates SET used = {r23} WHERE buryat = '{ww}'")
                        db.commit()

                    ff2 = -1
                else:
                    ww = str(message.text)
                    ww = ww.lower()

                    sql.execute(f"SELECT * FROM translates WHERE russian = '{ww}'")
                    translate_w = sql.fetchone()

                    if translate_w is None:
                        bot.send_message(
                            message.chat.id, 'К сожалению такого слова еще нет ):')
                    else:
                        bot.send_message(
                            message.chat.id, str(translate_w[1] + "\nэто слово переводили - " + str(translate_w[2]) + " человек!"))
                        r23 = translate_w[2] + 1
                        sql.execute(
                            f"UPDATE translates SET used = {r23} WHERE russian = '{ww}'")
                        db.commit()
                    ff2 = -1

                markup = types.InlineKeyboardMarkup(row_width=2)
                item1 = types.InlineKeyboardButton("Да", callback_data='y')
                item2 = types.InlineKeyboardButton("Нет", callback_data='n')

                markup.add(item1, item2)

                bot.send_message(
                    message.chat.id, 'Вы хотите перевести еще слова?', reply_markup=markup
                )

            if ff1 == True:
                # !ТУТ ПЕРЕВОД 
                if message.text == "Бурятский":
                    bot.send_message(
                        message.chat.id, 'ок теперь введи слово на бурятском и я его переведу! вот буквы которых нет на клавиатуре\nү\nһ\nө',
                        reply_markup=types.ReplyKeyboardRemove())
                    ff2 = 1
                    ff1 = False
                elif message.text == 'Русский':
                    bot.send_message(
                        message.chat.id, 'ок теперь введи на слово на русском и я его переведу!',
                        reply_markup=types.ReplyKeyboardRemove())
                    ff2 = 2
                    ff1 = False
                else:
                    bot.send_message(
                        message.chat.id, "пожалуйста введи язык из нижних кнопок"
                    )


            if message.text == "Перевод слов":
                ff1 = True

                markup = types.ReplyKeyboardMarkup(resize_keyboard=1)
                key1 = types.KeyboardButton('Бурятский')
                key2 = types.KeyboardButton('Русский')
                markup.add(key1, key2)

                bot.send_message(message.chat.id, 'Ок теперь выбери язык с которого нужно переводить', reply_markup=markup)

            if message.text == "Рандомный факт о Бурятии":
                # ?НУ ТУТ НАДО БРАТЬ ФАКТЫ ИЗ БУРЯТИИ ИЗ БД НО ПОКА ЧТО Я ДРУГИМ ЗАНЯТ
                pass
            if message.text == "Я хочу потренироваться":
                # ?В НОВОМ АПДЕЙТЕ
                pass

        @bot.callback_query_handler(func=lambda call: True)
        def callback_inline(call):
            db = sqlite3.connect("translate.db")
            sql = db.cursor()

            if call.message:
                if call.data == 'y':
                    global ff1
                    ff1 = True

                    markup = types.ReplyKeyboardMarkup(resize_keyboard=1)
                    key1 = types.KeyboardButton('Бурятский')
                    key2 = types.KeyboardButton('Русский')
                    markup.add(key1, key2)

                    bot.send_message(
                        call.message.chat.id, 'Ок теперь выбери язык с которого нужно переводить', reply_markup=markup)
                
                if call.data == 'n':
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                            text="Ок выбери язык и напиши текст который переводить", reply_markup=None)
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=1)
                    key1 = types.KeyboardButton("Перевод слов")
                    key2 = types.KeyboardButton("Я хочу потренероватся")
                    key3 = types.KeyboardButton("Рандомный факт о Бурятии")
                    markup.add(key1, key2, key3)

                    bot.send_message(call.message.chat.id, f"Привет!\nЯ бот который поможет тебе с бурятским языком.\nВыбери функцию которую ты хочешь что бы я выполнил", reply_markup=markup)


        bot.polling()
    except:
        pass