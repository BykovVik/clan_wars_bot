from config import bot, CAPTCHA_RANDOM_MAX, CAPTCHA_ERROR_MAX
from app import core
from telebot import types
import random

#Обработка нажатия кнопки "Зарегистрировать клан"
@bot.callback_query_handler(func=lambda call: call.data == "add_clan")
def add_clan(call):

    #Вызываем класс с базовыми методами приложения
    basic_methods = core.Core_Methods("chat", call.message.chat.id)
    #Проверяем БД на наличие чата с таким id
    check_chat = basic_methods.check_obj()
    #Если проверка вернула нам пустой масив, регистриуем чат
    if not check_chat:

        #Собираем данные для создания клана
        new_clan = [call.message.chat.title, call.message.chat.id, 0, False]
        #регистрируем клан
        basic_methods.reg_obj(new_clan)

        bot.send_message(call.message.chat.id, "Для полноценного функционирования игры, дайте боту ПРАВА АДМИНИСТРАТОРА")
        bot.delete_message(call.message.chat.id, call.message.message_id)
    else:
        bot.send_message(call.message.chat.id, "Клан уже зарегестрирован")
        bot.delete_message(call.message.chat.id, call.message.message_id)



#Обработка нажатия кнопки "Зарегистрировать юзера"
@bot.callback_query_handler(func=lambda call: call.data == "add_user")
def add_user(call):

    #Вызываем класс с базовыми методами приложения
    basic_methods = core.Core_Methods("chat", call.message.chat.id)
    #Проверяем БД на наличие чата с таким id
    check_chat = basic_methods.check_obj()
    #Если проверка вернула нам пустой масив, регистриуем чат
    if not check_chat:
        bot.send_message(call.message.chat.id, "Для того что бы регистрировать юзера, не обходимо что б от вашего чата должен быть зарегестрирован клан.")
        bot.delete_message(call.message.chat.id, call.message.message_id)
    else:
        #Вызываем класс с базовыми методами приложения
        basic_methods_user = core.Core_Methods("user", call.from_user.id)
        #Проверяем БД на наличие юзера с таким id
        check_user = basic_methods_user.check_obj()

        #Если проверка вернула нам пустой масив, регистриуем юзера
        if not check_user:
            #Собираем данные для создания юзера
            new_user = [call.from_user.first_name, call.from_user.id, 0, 0, 0, check_chat[0][0]]
            #регистрируем юзера
            basic_methods_user.reg_obj(new_user)

            bot.send_message(call.message.chat.id, "Регистрация юзера под ником {} произошла успешно".format(str(call.from_user.first_name)))
        else:
            bot.send_message(call.message.chat.id, "Юзер уже зарегестрирован")

        bot.delete_message(call.message.chat.id, call.message.message_id)


#Обработка нажатия кнопки "Удалить клан"
@bot.callback_query_handler(func=lambda call: call.data == "remove_clan")
def remove_clan(call):
    
    #Вызываем класс с базовыми методами приложения
    basic_methods = core.Core_Methods("chat", call.message.chat.id)
    #Проверяем БД на наличие чата с таким id
    check_chat = basic_methods.check_obj()
    #Если проверка вернула нам пустой масив, регистриуем чат
    if not check_chat:
        bot.send_message(call.message.chat.id, "Ваш чат не зарегистрирован как клан в игре 'Clan Wars'")
        bot.delete_message(call.message.chat.id, call.message.message_id)
    else:
        basic_methods.del_obj()
        bot.send_message(call.message.chat.id, "Клан успешно удалён")
        bot.delete_message(call.message.chat.id, call.message.message_id)



#Обработка нажатия кнопки "Удалить юзера"
@bot.callback_query_handler(func=lambda call: call.data == "remove_user")
def remove_user(call):

    #Вызываем класс с базовыми методами приложения
    basic_methods = core.Core_Methods("user", call.from_user.id)
    #Проверяем БД на наличие юзера с таким id
    check_user = basic_methods.check_obj()

    #Если проверка вернула нам пустой масив, регистриуем юзера
    if not check_user:
        bot.send_message(call.message.chat.id, "У вас нет зарегистрированного юзера")
    else:
        basic_methods.del_obj()
        bot.send_message(call.message.chat.id, "Юзер успешно удалён")

    bot.delete_message(call.message.chat.id, call.message.message_id)


#Обработка нажатия кнопки "Статистика игроков"
@bot.callback_query_handler(func=lambda call: call.data == "active_user")
def active_user(call):
    
    pass


#Обработка нажатия кнопки "Начать игру"
@bot.callback_query_handler(func=lambda call: call.data == "start_game")
def active_user(call):

    pass


#Обработка нажатия кнопки лайка
@bot.callback_query_handler(func=lambda call: call.data == "add_like")
def add_like(call):

    #Вызываем класс с базовыми методами приложения
    basic_methods = core.Core_Methods("user", call.from_user.id)
    #Проверяем БД на наличие юзера с таким id
    check_user = basic_methods.check_obj()

    #Если проверка вернула нам пустой масив, регистриуем юзера
    if not check_user:

        #Ответ на клабэк запрос
        bot.answer_callback_query(call.id)

    #Если поле active_captcha не пусто, значит у юзера нет возможности ставить лайк
    if check_user[0][4] != 0:

        #Ответ на клабэк запрос
        bot.answer_callback_query(call.id)

    #Создаем рандомайзер для вывода лайк боксов
    random_num = random.randint(1, CAPTCHA_RANDOM_MAX)

    if random_num == 1:
        
        #Вызываем каптчу
        captcha(call)
        #Создаем экземпляр класса User
        user = core.Users(call.from_user.id)
        #Ставим флаг означающий что наш пользователь сейчас занят разгадыванием каптчи
        user.active_captcha_change(1)
        #Ответ на клабэк запрос
        bot.answer_callback_query(call.id)

    else:

        #Выбираем из JSON файла
        like = call.message.json["reply_markup"]["inline_keyboard"][0][0]["text"].split("❤️")[1]
        #Добавляем лайк
        like = int(like) + 1

        keyboard = types.InlineKeyboardMarkup(row_width=1)
        button_like = types.InlineKeyboardButton(text="Поставить лайк ❤️ {}".format(str(like)), callback_data="add_like")
        keyboard.add(button_like)

        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=keyboard)

        #Ответ на клабэк запрос
        bot.answer_callback_query(call.id)



def captcha(call):

    #Создаём экземляр класса каптчи
    captcha = core.Captcha(call.from_user.id)
    #Формируем Аудио и варианты ответов для каптчи
    audio_pack = captcha.get_captcha_construct()
    
    keyboard = types.InlineKeyboardMarkup(row_width=1)

    button_one = types.InlineKeyboardButton(text=audio_pack[1], callback_data="true")
    button_two = types.InlineKeyboardButton(text=audio_pack[2], callback_data="false")
    button_three = types.InlineKeyboardButton(text=audio_pack[3], callback_data="false")
    button_four = types.InlineKeyboardButton(text=audio_pack[4], callback_data="false")

    keyboard.add(button_one, button_two, button_three, button_four)

    #Отсылаем каптчу в личные сообщения пользователю
    bot.send_audio(call.from_user.id, open(audio_pack[0], 'rb'), reply_markup=keyboard)

    #Оповещаем пользователя в чате о том, что ему нужно зайти в личные сообщения
    bot.send_message(call.message.chat.id, "Приветсвую тебя {}, пройди эту капчу что б я знал что ты не бот. Три бала за неверно пройденную капчу онулируют ваш баланс".format(str(call.from_user.first_name)))


#Обработка нажатия кнопки верного ответа
@bot.callback_query_handler(func=lambda call: call.data == "true")
def true_captcha(call):
    
    #Создаем экземпляр класса User
    user = core.Users(call.from_user.id)
    #Ставим флаг, обозначающий что юзер НЕ занят капчей
    user.active_captcha_change(0)
    #Ответ на клабэк запрос
    bot.answer_callback_query(call.id, text="Каптча пройдена успешно")
    bot.delete_message(call.from_user.id, call.message.message_id)


#Обработка нажатия кнопки НЕ верного ответа
@bot.callback_query_handler(func=lambda call: call.data == "false")
def false_captcha(call):
    
    #Cоздаем экземпляр класса User
    user = core.Users(call.from_user.id)
    #Ставим флаг, обозначающий что юзер НЕ занят капчей
    user.active_captcha_change(0)
    #Получаем количество ошибок, допущщеных приразгадывании каптчи
    captcha_errors = user.get_sum_captcha_error()

    #Если количество ошибок достигло критической точки
    if captcha_errors == CAPTCHA_ERROR_MAX:

        #Онулируем очки юзера
        user.update_items(0)
        #Ответ на клабэк запрос
        bot.answer_callback_query(call.id, text="ОШИБКА КАПТЧИ(количество: {}) Ваши очки онулированы".format(str(captcha_errors)))
        bot.delete_message(call.from_user.id, call.message.message_id)

    else:

        #Добавляем только что допущенную ошибку
        captcha_errors += 1
        #Подсчитываем ошибки юзера
        user.captcha_error_change(captcha_errors)
        #Ответ на клабэк запрос
        bot.answer_callback_query(call.id, text="ОШИБКА КАПТЧИ(количество: {})".format(str(captcha_errors)))
        bot.delete_message(call.from_user.id, call.message.message_id)