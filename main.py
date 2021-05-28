import config
import telebot
from telebot import types
from app import core


#Создаём экземпляр бота
bot = telebot.TeleBot(config.TOKEN)


#Обработка первого появления Бота в чате
@bot.message_handler(content_types=['new_chat_members'])
def reg_chat(message):

    if message.new_chat_members[0].id == bot.get_me().id:
        #Вызываем класс Чат
        this_chat = core.Clan_Stats(message)
        #Проверяем БД на наличие чата с таким id
        check_chat = this_chat.check_chats()
        #Если проверка вернула нам пустой масив, регистриуем чат
        if not check_chat:
            this_chat.reg_clan()
            bot.send_message(message.chat.id, "Для полноценного функционирования игры, дайте боту ПРАВА АДМИНИСТРАТОРА")
        else:
            bot.send_message(message.chat.id, "Клан уже зарегестрирован")


#Обработка команды /help
@bot.message_handler(commands=['help'])
def help_message(message):
    
    bot.send_message(message.chat.id, "Правила игры")


#Обработка команды /start
@bot.message_handler(commands=['start'])
def help_message(message):

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    button_reg = types.InlineKeyboardButton(text="Зарегистрировать клан", callback_data="add_clan")
    button_reg_user = types.InlineKeyboardButton(text="Зарегистрировать юзера", callback_data="add_user")
    button_active_user = types.InlineKeyboardButton(text="Статистика игроков", callback_data="remove_clan")
    button_start_game = types.InlineKeyboardButton(text="Начать игру", callback_data="remove_clan")
    button_del = types.InlineKeyboardButton(text="Удалить клан", callback_data="remove_clan")
    button_del_user = types.InlineKeyboardButton(text="Удалить клан", callback_data="remove_clan")
    keyboard.add(button_reg, button_reg_user, button_active_user, button_start_game, button_del, button_del_user)
    
    bot.send_message(message.chat.id, "Правила игры", reply_markup=keyboard)


#Обработка нажатия кнопки "Зарегистрировать клан"
@bot.callback_query_handler(func=lambda call: call.data == "add_clan")
def add_clan(call):
    #Вызываем класс Чат
    this_chat = core.Clan_Stats(call.message)
    #Проверяем БД на наличие чата с таким id
    check_chat = this_chat.check_chats()
    #Если проверка вернула нам пустой масив, регистриуем чат
    if not check_chat:
        this_chat.reg_clan()
        bot.send_message(call.message.chat.id, "Для полноценного функционирования игры, дайте боту ПРАВА АДМИНИСТРАТОРА")
        bot.delete_message(call.message.chat.id, call.message.message_id)
    else:
        bot.send_message(call.message.chat.id, "Клан уже зарегестрирован")
        bot.delete_message(call.message.chat.id, call.message.message_id)


#Обработка нажатия кнопки "Зарегистрировать юзера"
@bot.callback_query_handler(func=lambda call: call.data == "add_user")
def add_clan(call):
    #Вызываем класс Чат
    this_chat = core.Clan_Stats(call.message)
    #Проверяем БД на наличие чата с таким id
    check_chat = this_chat.check_chats()
    #Если проверка вернула нам пустой масив, регистриуем чат
    if not check_chat:
        bot.send_message(call.message.chat.id, "Для того что бы регистрировать юзера, не обходимо что б от вашего чата должен быть зарегестрирован клан.")
        bot.delete_message(call.message.chat.id, call.message.message_id)
    else:
        #Вызываем класс User
        this_user = core.Player_Stats(call.message)
        #Проверяем БД на наличие юзера с таким id
        check_user = this_user.check_players()

        #Если проверка вернула нам пустой масив, регистриуем юзера
        if not check_user:
            this_user.reg_user(check_chat[0][0])
            bot.send_message(call.message.chat.id, "Регистрация юзера под ником {} произошла успешно".format(str(call.from_user.first_name)))
        else:
            bot.send_message(call.message.chat.id, "Юзер уже зарегестрирован")

        bot.delete_message(call.message.chat.id, call.message.message_id)


#Обработка нажатия кнопки "Удалить клан"
@bot.callback_query_handler(func=lambda call: call.data == "remove_clan")
def remove_clan(call):
    #Вызываем класс Чат
    this_chat = core.Clan_Stats(call.message)
    #Проверяем БД на наличие чата с таким id
    check_chat = this_chat.check_chats()
    #Если проверка вернула нам пустой масив, регистриуем чат
    if not check_chat:
        this_chat.reg_clan()
        bot.send_message(call.message.chat.id, "Ваш чат не зарегистрирован как клан в игре 'Clan Wars'")
        bot.delete_message(call.message.chat.id, call.message.message_id)
    else:
        this_chat.del_clan()
        bot.send_message(call.message.chat.id, "Клан успешно удалён")
        bot.delete_message(call.message.chat.id, call.message.message_id)



#Обработка нажатия кнопки "Удалить юзера"
@bot.callback_query_handler(func=lambda call: call.data == "remove_user")
def remove_user(call):
    #Вызываем класс User
    this_user = core.Player_Stats(call.message)
    #Проверяем БД на наличие юзера с таким id
    check_user = this_user.check_players()

    #Если проверка вернула нам пустой масив, регистриуем юзера
    if not check_user:
        bot.send_message(call.message.chat.id, "У вас нет зарегистрированного юзера")
    else:
        this_user.del_user()
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
def check_chat_message(message):

    pass


#Запуск функции опрашивающей сервер Telegram
if __name__ == "__main__":
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
        print("Ошибка пришла из точки входа")
