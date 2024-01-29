import telebot
from telebot import types
import os, random
import pyttsx3
import pythoncom


bot = telebot.TeleBot('YOUR TOKEN')


# команды бота
bot.set_my_commands([
    telebot.types.BotCommand("/start", "Темы изучения"),
    telebot.types.BotCommand("/help", "Помощь"),
    telebot.types.BotCommand('/letter', 'Письмо разработчикам'),
])

USRLIST = {}
message_list = {}
groups = {}


# обработчик команды "start"
@bot.message_handler(commands=['start'])
def start(message):
    kb = types.InlineKeyboardMarkup(row_width=2)
    btn2 = types.InlineKeyboardButton(text='Профессии', callback_data='btn2')
    btn4 = types.InlineKeyboardButton(text='Транспорт', callback_data='btn4')
    btn5 = types.InlineKeyboardButton(text='Цвета', callback_data='btn5')
    btn6 = types.InlineKeyboardButton(text='Погода', callback_data='btn6')
    kb.add(btn2, btn4, btn5, btn6)
    bot.send_message(message.chat.id, 'Добро пожаловать!\nЧто изучим сегодня?', reply_markup=kb)

    USRLIST[message.chat.id] = '0'
    print(USRLIST)


# обработчик команды "help"
@bot.message_handler(commands=['help'])
def help(message):
        bot.send_message(message.chat.id, 'Справка по работе с ботом: \n/start для начала работы или выбора новой темы изучения \n/help - для вызова справки \n/letter - письмо разработчикам')


# обработчик команды "letter"
@bot.message_handler(commands=['letter'])
def letter(message):
    sent = bot.send_message(message.chat.id, 'Напишите пожалуйста ваши пожелания по улучшению бота, все предложения будут рассмотрены')
    bot.register_next_step_handler(sent, review)

def review(message):
    message_to_save = message.text
    with open('letter.txt', 'a') as tx:
        print(message_to_save, file=tx)
        bot.send_message(message.chat.id, 'Спасибо, Ваше сообщение будет рассмотрено! \nДля продолжения нажмите "Следующее слово"')
        bot.register_next_step_handler(message, answer1)



# обработчик кнопок меню. Открытие каталога, соответствующего кнопке меню
@bot.callback_query_handler(func=lambda callback: True)
def randome_coll(callback):
    global c_back
    groups[callback.from_user.id] = callback.data
    c_back = groups.get(callback.from_user.id)
    if c_back == 'btn2':            # кнопка Profession
        photo = open('eng/professions/' + random.choice(os.listdir('eng/professions/')), 'rb')  # открытие каталога и выбор файла
        change1 = os.path.basename(photo.name)
        change2 = change1.index('.')
        photo_name = change1[:change2]
        bot.send_photo(callback.from_user.id, photo)  # отправляем фото
        USRLIST[callback.from_user.id] = photo_name
        photo.close()
        kl = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        kn = types.KeyboardButton(text='Показать правильный ответ')
        kl.add(kn)
        bot.send_message(callback.from_user.id, 'Напишите на английском', reply_markup=kl)

    elif c_back == 'btn4':            # кнопка Transport
        photo = open('eng/transports/' + random.choice(os.listdir('eng/transports/')), 'rb')
        change1 = os.path.basename(photo.name)
        change2 = change1.index('.')
        photo_name = change1[:change2]
        bot.send_photo(callback.from_user.id, photo)
        USRLIST[callback.from_user.id] = photo_name
        photo.close()
        kl = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        kn = types.KeyboardButton(text='Показать правильный ответ')
        kl.add(kn)
        bot.send_message(callback.from_user.id, 'Напишите на английском', reply_markup=kl)

    elif c_back == 'btn5':            # кнопка Colors
        photo = open('eng/colors/' + random.choice(os.listdir('eng/colors/')), 'rb')
        change1 = os.path.basename(photo.name)
        change2 = change1.index('.')
        photo_name = change1[:change2]
        bot.send_photo(callback.from_user.id, photo)
        USRLIST[callback.from_user.id] = photo_name
        photo.close()
        kl = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        kn = types.KeyboardButton(text='Показать правильный ответ')
        kl.add(kn)
        bot.send_message(callback.from_user.id, 'Напишите на английском', reply_markup=kl)

    elif c_back == 'btn6':            # кнопка Nature
        photo = open('eng/nature/' + random.choice(os.listdir('eng/nature/')), 'rb')
        change1 = os.path.basename(photo.name)
        change2 = change1.index('.')
        photo_name = change1[:change2]
        bot.send_photo(callback.from_user.id, photo)
        USRLIST[callback.from_user.id] = photo_name
        photo.close()
        kl = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        kn = types.KeyboardButton(text='Показать правильный ответ')
        kl.add(kn)
        bot.send_message(callback.from_user.id, 'Напишите на английском', reply_markup=kl)

    else:
        bot.send_message(callback.from_user.id, 'Выберите тему изучения')



@bot.message_handler(content_types=['text'])
def answer(message):
    message_list[message.chat.id] = message.text
    user = USRLIST.get(message.chat.id)
    if message.text.casefold() == USRLIST.get(message.chat.id):
        kl = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        kn = types.KeyboardButton(text='Следующее слово')
        kn2 = types.KeyboardButton(text='🎤🎵 Произнести')
        kl.add(kn2, kn)
        bot.send_message(message.chat.id, 'Верно', reply_markup=kl)
        bot.register_next_step_handler(message, answer1)

    elif message.text == 'Показать правильный ответ':
        bot.send_message(message.chat.id, 'Правильный ответ: {}'.format(user.capitalize()))
        bot.send_message(message.chat.id, 'Для продолжения введите правильный ответ')
        bot.register_next_step_handler(message, answer)

    elif message.text == '/start':
        kb = types.InlineKeyboardMarkup(row_width=2)
        btn2 = types.InlineKeyboardButton(text='Профессии', callback_data='btn2')
        btn4 = types.InlineKeyboardButton(text='Транспорт', callback_data='btn4')
        btn5 = types.InlineKeyboardButton(text='Цвета', callback_data='btn5')
        btn6 = types.InlineKeyboardButton(text='Природа', callback_data='btn6')
        kb.add(btn2, btn4, btn5, btn6)
        bot.send_message(message.chat.id, 'Что изучим сегодня?', reply_markup=kb)

    elif message.text == '/help':
        bot.send_message(message.chat.id, 'Справка по работе с ботом: \n/start для начала работы или выбора новой темы изучения \n/help - для вызова справки \n/letter - письмо разработчикам, с предложениями по улучшению бота')

    elif message.text == '/letter':
        sent = bot.send_message(message.chat.id, 'Напишите пожалуйста ваши пожелания по улучшению бота, все предложения будут рассмотрены')
        bot.register_next_step_handler(sent, review)

    else:
        bot.send_message(message.from_user.id, 'Не верно')
        bot.register_next_step_handler(message, answer)


# Обработчик перехода к следующему слову, и озвучивание
@bot.message_handler(func=lambda message: message.text == 'Следующее слово' or '🎤🎵 Произнести')
def answer1(message):
    if message.text == 'Следующее слово':
        c_back = groups.get(message.from_user.id)
        if c_back == 'btn2':
            photo = open('eng/professions/' + random.choice(os.listdir('eng/professions/')), 'rb')
            change1 = os.path.basename(photo.name)
            change2 = change1.index('.')
            photo_name = change1[:change2]
            bot.send_photo(message.from_user.id, photo)
            USRLIST[message.from_user.id] = photo_name
            photo.close()
            kl = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            kn = types.KeyboardButton(text='Показать правильный ответ')
            kl.add(kn)
            bot.send_message(message.chat.id, 'Напишите на английском', reply_markup=kl)
            bot.register_next_step_handler(message, answer2)

        elif c_back == 'btn5':
            photo = open('eng/colors/' + random.choice(os.listdir('eng/colors/')), 'rb')
            change1 = os.path.basename(photo.name)
            change2 = change1.index('.')
            photo_name = change1[:change2]
            bot.send_photo(message.from_user.id, photo)
            USRLIST[message.from_user.id] = photo_name
            photo.close()
            kl = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            kn = types.KeyboardButton(text='Показать правильный ответ')
            kl.add(kn)
            bot.send_message(message.chat.id, 'Напишите на английском', reply_markup=kl)
            bot.register_next_step_handler(message, answer2)


        elif c_back == 'btn4':
            photo = open('eng/transports/' + random.choice(os.listdir('eng/transports/')), 'rb')
            change1 = os.path.basename(photo.name)
            change2 = change1.index('.')
            photo_name = change1[:change2]
            bot.send_photo(message.from_user.id, photo)
            USRLIST[message.from_user.id] = photo_name
            photo.close()
            kl = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            kn = types.KeyboardButton(text='Показать правильный ответ')
            kl.add(kn)
            bot.send_message(message.chat.id, 'Напишите на английском', reply_markup=kl)
            bot.register_next_step_handler(message, answer2)


        elif c_back == 'btn6':
            photo = open('eng/nature/' + random.choice(os.listdir('eng/nature/')), 'rb')
            change1 = os.path.basename(photo.name)
            change2 = change1.index('.')
            photo_name = change1[:change2]
            bot.send_photo(message.from_user.id, photo)
            USRLIST[message.from_user.id] = photo_name
            photo.close()
            kl = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            kn = types.KeyboardButton(text='Показать правильный ответ')
            kl.add(kn)
            bot.send_message(message.chat.id, 'Напишите на английском', reply_markup=kl)
            bot.register_next_step_handler(message, answer2)


    elif message.text == '🎤🎵 Произнести':           # команда голосового озвучивания слова
        pythoncom.CoInitialize()
        user = USRLIST.get(message.chat.id)
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('rate', 115)
        engine.setProperty('voice', voices[2].id)
        r1 = random.randint(1,10000000)
        voice = 'voice'+str(r1) +'.ogg'
        engine.save_to_file(user, voice)
        engine.runAndWait()
        with open(str(voice), 'rb') as audio:
            bot.send_voice(message.from_user.id, audio)
            audio.close()
        bot.register_next_step_handler(message, answer1)

    elif message.text == '/start':
        kb = types.InlineKeyboardMarkup(row_width=2)
        btn2 = types.InlineKeyboardButton(text='Профессии', callback_data='btn2')
        btn4 = types.InlineKeyboardButton(text='Транспорт', callback_data='btn4')
        btn5 = types.InlineKeyboardButton(text='Цвета', callback_data='btn5')
        btn6 = types.InlineKeyboardButton(text='Природа', callback_data='btn6')

        kb.add(btn2, btn4, btn5, btn6)
        bot.send_message(message.chat.id, 'Что изучим сегодня?', reply_markup=kb)


    elif message.text == '/help':
        bot.send_message(message.chat.id, 'Перед Вами демо-версия языкового бота Write a Word - t.me/WriteWordBot, \nс его помощью Вы сможете изучить 1000 самых распространенных слов английского языка, слова разбиты по темам и имеют яркие фотокарточки, благодаря которым запоминаемое слово приобретает визуальный образ и закрепляется в памяти. Так же, каждое слово можно воспроизвести встроенным голосовым помощником, позволяющим тренировать правильное произношение изученных слов. \nДемо-версия представлена для ознакомления с функционалом бота Write a Word, по этому она имеет ограничение по количеству групп слов - 4 группы, в каждой из которых по 5 карточек.\n\nСправка по работе с ботом: \n/start для начала работы или выбора новой темы изучения \n/help - для вызова справки \n/letter - письмо разработчикам, с предложениями по улучшению бота\nP.S. кнопки меню доступны, когда бот не ждет от Вас ответа на карточку.')

    elif message.text == '/letter':
        sent = bot.send_message(message.chat.id, 'Напишите пожалуйста ваши пожелания по улучшению бота, все предложения будут рассмотрены')
        bot.register_next_step_handler(sent, review)


    else:
        bot.send_message(message.chat.id, 'Нажмите "Произнести", или "Следующее слово"')
        bot.register_next_step_handler(message, answer1)


def answer2(message):
    message_list[message.chat.id] = message.text
    user = USRLIST.get(message.chat.id)
    if message.text.casefold() == USRLIST.get(message.chat.id):
        kl = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        kn = types.KeyboardButton(text='Следующее слово')
        kn2 = types.KeyboardButton(text='🎤🎵 Произнести')
        kl.add(kn2, kn)
        bot.send_message(message.chat.id, 'Верно', reply_markup=kl)
        bot.register_next_step_handler(message, answer1)
    elif message.text == 'Показать правильный ответ':
        bot.send_message(message.chat.id, 'Правильный ответ: {}'.format(user.capitalize()))
        bot.send_message(message.chat.id, 'Для продолжения введите правильный ответ')
        bot.register_next_step_handler(message, answer2)
    else:
        bot.send_message(message.from_user.id, 'Нет')
        bot.register_next_step_handler(message, answer2)





bot.polling(none_stop=True)



