import vk_api
from vk_api import keyboard
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
import random
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import Levenshtein
import bot_tokens

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
dictionary = [['привет', 'сайн байна'], ['пока', 'баяртай'],
              ['работа', 'ажал'],
              ['ручка', 'гархан'], ['пенал', 'пенал'],
              ['тетрадь', 'дэбтэр'], ['учебник', 'ном'],
              ['карандаш', 'харандааш'], ['учитель', 'багша'],
              ['учительская', 'багшанарай таһалга'], ['директор', 'дарга'],
              ['ученик', 'һурагша'], ['завуч', 'завуч'],
              ['английский язык', 'англи хэлэн'], [
                  'бурятский', 'буряадай хэлэн'],
              ['русский язык', 'ородой хэлэн'], ['школа', 'һургуули']
              ]

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


def create_keyboard(response):
    keyboard = VkKeyboard(one_time=False)

    if response == 'тест':

        keyboard.add_button('Русский', color=VkKeyboardColor.DEFAULT)
        keyboard.add_button('Бурятский', color=VkKeyboardColor.DEFAULT)
        keyboard.add_button('Английский', color=VkKeyboardColor.DEFAULT)

    elif response == 'закрыть':
        print('закрываем клаву')
        return keyboard.get_empty_keyboard()

    keyboard = keyboard.get_keyboard()
    return keyboard


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


authorize = vk_api.VkApi(token=token)
longpoll = VkLongPoll(authorize)
gb = 0
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        received_message = event.text.lower()
        sender = event.user_id
        if gb:
            pass
        else:
            if received_message == "Русский":
                kbd = create_keyboard("закрыть")
                authorize.method('messages.send', {
                    'user_id': sender, 'message': "Теперь пиши слова", 'random_id': get_random_id(), 'keyboard': kbd})
                ind1 = 0, ind2 = 1
                gb = True
            elif received_message == "Бурятский":
                kbd = create_keyboard("закрыть")
                authorize.method('messages.send', {
                    'user_id': sender, 'message': "Теперь пиши слова", 'random_id': get_random_id(), 'keyboard': kbd})

                ind1 = 1, ind2 = 0
                gb = True

            elif received_message == "Английский":
                kbd = create_keyboard("закрыть")
                authorize.method('messages.send', {
                    'user_id': sender, 'message': "Теперь пиши слова", 'random_id': get_random_id(), 'keyboard': kbd})

                ind1 = 2, ind2 = 1
                gb = True


            else:
                keyboard = create_keyboard('тест')
                authorize.method('messages.send', {
                    'user_id': sender, 'message': "Выбери язык из кнопок внизу", 'random_id': get_random_id(), 'keyboard': keyboard})

        # write_message(sender, ans)
            #send_sticker(sender, stickers[random.randint(0, 22)])
