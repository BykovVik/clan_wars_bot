from os import link
import time
import random
import config
import telebot
from telebot import types
from telebot.util import async_dec
from app import core


#Создаём экземпляр бота
bot = telebot.TeleBot(config.TOKEN)


#Обработка первого появления Бота в чате
@bot.message_handler(content_types=['new_chat_members'])
def reg_chat(message):

    if message.new_chat_members[0].id == bot.get_me().id:

        #Вызываем класс с базовыми методами приложения
        basic_methods = core.Core_Methods("chat", message.chat.id)
        #Проверяем БД на наличие чата с таким id
        check_chat = basic_methods.check_obj()
        #Если проверка вернула нам пустой масив, регистриуем чат
        if not check_chat:
            new_clan = [message.chat.title, message.chat.id, 0, False]
            basic_methods.reg_obj(new_clan)
            bot.send_message(message.chat.id, "Для полноценного функционирования игры, дайте боту ПРАВА АДМИНИСТРАТОРА")
        else:
            bot.send_message(message.chat.id, "Клан уже зарегестрирован")


#Обработка команды /help
@bot.message_handler(commands=['help'])
def help_message(message):

    if message.chat.type == 'private':
    
        bot.send_message(message.chat.id, "Бот работает исключительно в чате")

    else:

        bot.send_message(message.chat.id, "Правила игры")



#Обработка команды /start
@bot.message_handler(commands=['start'])
def help_message(message):

    if message.chat.type == 'private':
    
        bot.send_message(message.chat.id, "Бот работает исключительно в чате")

    else:

        keyboard = types.InlineKeyboardMarkup(row_width=1)
        button_reg = types.InlineKeyboardButton(text="Зарегистрировать клан", callback_data="add_clan")
        button_reg_user = types.InlineKeyboardButton(text="Зарегистрировать юзера", callback_data="add_user")
        button_active_user = types.InlineKeyboardButton(text="Статистика игроков", callback_data="remove_clan")
        button_start_game = types.InlineKeyboardButton(text="Начать игру", callback_data="remove_clan")
        button_del = types.InlineKeyboardButton(text="Удалить клан", callback_data="remove_clan")
        button_del_user = types.InlineKeyboardButton(text="Удалить юзера", callback_data="remove_user")
        keyboard.add(button_reg, button_reg_user, button_active_user, button_start_game, button_del, button_del_user)
        
        bot.send_message(message.chat.id, "Правила игры", reply_markup=keyboard)


#Обработка нажатия кнопки "Зарегистрировать клан"
@bot.callback_query_handler(func=lambda call: call.data == "add_clan")
def add_clan(call):

    #Вызываем класс с базовыми методами приложения
    basic_methods = core.Core_Methods("chat", call.message.chat.id)
    #Проверяем БД на наличие чата с таким id
    check_chat = basic_methods.check_obj()
    #Если проверка вернула нам пустой масив, регистриуем чат
    if not check_chat:
        new_clan = [call.message.chat.title, call.message.chat.id, 0, False]
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
            new_user = [call.from_user.first_name, call.from_user.id, 0, check_chat[0][0]]
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


#Обработка сообщений чата
@bot.message_handler(content_types=['text', 'photo', 'voice', 'audio', 'document'])
@async_dec()
def check_chat_message(message):

    #Если человек пишет боту в личные сообщения
    if message.chat.type == 'private':
    
        return

    #Вызываем класс с базовыми методами приложения
    basic_methods = core.Core_Methods("user", message.from_user.id)
    #Проверяем БД на наличие юзера с таким id
    check_user = basic_methods.check_obj()

    #Если проверка вернула нам пустой масив - завершаем функцию
    if not check_user:

        return

    chat = core.Clans(message.chat.id)
    chat_status = chat.get_active_status()

    #Если активность чата не нулевая - завершаем функцию
    if chat_status != 0:

        return

    random_num = random.randint(1, config.LIKE_BOX_RANDOM_MAX)

    if random_num != 1:

        return

    like = 0
    chat.active_status_change(True)

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    button_like = types.InlineKeyboardButton(text="Поставить лайк ❤️ {}".format(str(like)), callback_data="add_like")
    keyboard.add(button_like)

    forw_mes = bot.forward_message(chat_id=message.chat.id, from_chat_id=message.chat.id, message_id=message.message_id)

    send_mes = bot.send_message(message.chat.id, "Поддержи друга {} лайком".format(message.from_user.first_name), reply_markup=keyboard)

    start = time.monotonic()

    while True:

        if time.monotonic() - start > 20:

            chat.active_status_change(False)

            try:

                bot.delete_message(message.chat.id, forw_mes.id)
                bot.delete_message(message.chat.id, send_mes.id)

            except:

                print("Отработал таймер на Лайк Боксе")
                return



#Обработка нажатия кнопки лайка
@bot.callback_query_handler(func=lambda call: call.data == "add_like")
def add_like(call):
    
    #Выбираем из JSON файла
    like = call.message.json["reply_markup"]["inline_keyboard"][0][0]["text"].split("❤️")[1]
    like = int(like) + 1

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    button_like = types.InlineKeyboardButton(text="Поставить лайк ❤️ {}".format(str(like)), callback_data="add_like")
    keyboard.add(button_like)

    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=keyboard)

    exit_like_box(call)


def exit_like_box(call):

    bot.answer_callback_query(call.id)
    return



#Запуск функции опрашивающей сервер Telegram
if __name__ == "__main__":
    
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
        print("Ошибка пришла из точки входа")
