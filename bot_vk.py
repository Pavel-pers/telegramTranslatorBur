import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from fuzzywuzzy import fuzz
import Levenshtein
import bot_tokens
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import sqlite3 as sql
import time


token = bot_tokens.vk


def write_message(sender, message):
    authorize.method('messages.send', {
                     'user_id': sender, 'message': message, 'random_id': get_random_id()})


def send_sticker(sender, sticker_id):
    authorize.method('messages.send', {
                     'user_id': sender, 'sticker_id': sticker_id, 'random_id': get_random_id()})


stickers = [80, 21355, 61, 8334, 11748, 21369, 21363, 15802, 15810, 1457, 1460, 21402, 51258, 13482, 13066, 13747,
            15249, 16940, 7379, 14268, 4340, 9015, 9032]  # номера стикеров


ind1 = 0
ind2 = 1
rus_bur = ['русский', 'бурятский']
con = sql.connect('_DB.db')

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

bur_letters = ['ү', 'ө', 'һ']
# үөһ


def num_to_word(a):
    lst = [int(i) for i in list(a)]
    n = len(lst)
    ans = ""
    if n > 7:
        return "error404, число слишком большое (лимит чисел - 1-1000000)"
    for i in range(0, n):
        ans += ((numb_names[0 if (n - i - 1) % 3 != 1 else 1]
                 [lst[i]] + numb_suffixes[n - 1 - i]) if lst[i] else "") + " "
    ans = ans.rstrip()
    return ans

def get_name(uid: int) -> str:
    data = authorize.method("users.get", {"user_ids": uid})[0]
    return "{} {}".format(data["first_name"], data["last_name"])

authorize = vk_api.VkApi(token=token)
longpoll = VkLongPoll(authorize)
def create_keyboard(response):
    keyboard = VkKeyboard(one_time=False)

    if response == 'тест':

        keyboard.add_button('Русский', color=VkKeyboardColor.SECONDARY)
        keyboard.add_button('Бурятский', color=VkKeyboardColor.SECONDARY)
        keyboard.add_button('Английский', color=VkKeyboardColor.SECONDARY)

    elif response == 'закрыть':
        return keyboard.get_empty_keyboard()

    keyboard = keyboard.get_keyboard()
    return keyboard
gb = 0

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        received_message = event.text.lower()
        sender = event.user_id
        print(f"{get_name(sender)} написал - <{received_message}>")
        if gb:
            nw_qn = time.time()

            flg = 0
            for i in received_message:
                if ord('0') > ord(i) or ord(i) > ord('9'):
                    flg = 1
                    break
            if not flg:
                write_message(sender, num_to_word(received_message))
                continue
            received_message_a = ''
            for i in range(len(received_message)):
                if ord('а') <= ord(received_message[i]) <= ord('я') or received_message[i] == 'ё' or received_message[i] in bur_letters or ord('a') <= ord(received_message[i]) <= ord('z'):
                    received_message_a += received_message[i]
                    continue
                else:
                    received_message_a += ' '

            words = [i.strip() for i in received_message_a.split()]
            if len(words) == 0:
                write_message(
                    sender, "Я вас не понимаю... Скорее всего, этого слова нет в словаре")
                send_sticker(sender, stickers[0])
            #print(words, received_message)
            if flg:
                ans = ''

                for i in words:
                    mx = 0
                    str1 = ''

                    erhgj = time.time()    
                    with con:
                        cur = con.cursor()
                        cur.execute("SELECT * FROM translates")
                        rows = cur.fetchall()
                        o = 0
                        strdp = ''
                        for j in rows:
                            ratio = fuzz.token_sort_ratio(i, j[ind1])
                            if ratio > mx:
                                mx = ratio
                                str1 = j[ind1]
                                str2 = j[ind2]
                                strdp = j[3 - ind1 - ind2]
                        con.commit()
                        cur.close()
                    if mx >= 58:
                        print(
                            f"из <{str1}> в <{str2}> другой перевод - <{strdp}>\nВремя затраченное на перевод %s" % round((time.time() - erhgj),2))
                    if mx == 100:
                        ans += str2 + ', '
                    elif mx >= 58:
                        ans += str2 + ' (возможно, вы имели ввиду ' + str1 + '), '
                    else:
                        ans += '?, '

                ans = ans[:-2]
                write_message(sender, ans)
                #send_sticker(sender, stickers[random.randint(0, 22)])
            gb = 0
            keyboard = create_keyboard('тест')
            authorize.method('messages.send', {
                    'user_id': sender, 'message': "Выбери язык из кнопок внизу", 'random_id': get_random_id(), 'keyboard': keyboard})
            print("Время отклика на перевод %s" % round((time.time() - nw_qn), 2))

        else:
            if received_message == "русский":
                kbd = create_keyboard("закрыть")
                authorize.method('messages.send', {
                    'user_id': sender, 'message': "Теперь пиши слова", 'random_id': get_random_id(), 'keyboard': kbd})
                ind1 = 0
                ind2 = 1
                gb = True
            elif received_message == "бурятский":
                kbd = create_keyboard("закрыть")
                authorize.method('messages.send', {
                    'user_id': sender, 'message': "Теперь пиши слова", 'random_id': get_random_id(), 'keyboard': kbd})

                ind1 = 1
                ind2 = 0
                gb = True

            elif received_message == "английский":
                kbd = create_keyboard("закрыть")
                authorize.method('messages.send', {
                    'user_id': sender, 'message': "Теперь пиши слова", 'random_id': get_random_id(), 'keyboard': kbd})

                ind1 = 2
                ind2 = 1
                gb = True


            else:
                keyboard = create_keyboard('тест')
                authorize.method('messages.send', {
                    'user_id': sender, 'message': "Выбери язык из кнопок внизу", 'random_id': get_random_id(), 'keyboard': keyboard})


