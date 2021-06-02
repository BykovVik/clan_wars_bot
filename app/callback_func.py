from config import bot
from app import core
from telebot import types

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


#Обработка нажатия кнопки лайка
@bot.callback_query_handler(func=lambda call: call.data == "add_like")
def add_like(call):
    
    #Выбираем из JSON файла
    like = call.message.json["reply_markup"]["inline_keyboard"][0][0]["text"].split("❤️")[1]
    #Добавляем лайк
    like = int(like) + 1

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    button_like = types.InlineKeyboardButton(text="Поставить лайк ❤️ {}".format(str(like)), callback_data="add_like")
    keyboard.add(button_like)

    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=keyboard)

    exit_like_box(call)


def exit_like_box(call):

    bot.answer_callback_query(call.id)
    return