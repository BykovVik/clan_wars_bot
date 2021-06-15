from app.core import Core_Methods, Users, Clans
from app.config import bot

class Check_Callback_Functions:

    def __init__(self, call):

        self.call = call


    def check_user(self):

        #Вызываем класс с базовыми методами приложения
        basic_methods = Core_Methods("user", self.call.from_user.id)
        #Проверяем БД на наличие юзера с таким id
        check_user = basic_methods.check_obj()

        #Если проверка вернула нам пустой масив, регистриуем юзера
        if not check_user:

            #Ответ на клабэк запрос
            bot.answer_callback_query(self.call.id, "У тебя нет зарегистрированного юзера")
            return False

        if self.call.message.chat.type != 'private':

            #Если чат юзера не совпадает с ID того чата в котором он находится
            if check_user[0].users_clan != self.call.message.chat.id:

                #Ответ на клабэк запрос
                bot.answer_callback_query(self.call.id, "Ты играешь за другой клан")
                return False

        #Если юзер не активировал аккаунт в личных сообщениях с ботом
        if check_user[0].user_activation == 0:

            if self.call.message.chat.type == 'private':

                return False

            #Ответ на клабэк запрос
            bot.answer_callback_query(self.call.id, "Активируй свой аккаунт в личных сообщениях с ботом")
            return False

        else:

            #Ответ на клабэк запрос
            bot.answer_callback_query(self.call.id, "Аккаует уже активирован")
            return True


        return True


    def check_admin(self):

        res = bot.get_chat_administrators(self.call.message.chat.id)

        for i in res:

            if i.user.id == self.call.from_user.id:

                return True

        return False


    def check_clan(self, true_answer, false_answer):

        #Вызываем класс с базовыми методами приложения
        basic_methods = Core_Methods("chat", self.call.message.chat.id)
        #Проверяем БД на наличие чата с таким id
        check_chat = basic_methods.check_obj()

        #Если проверка вернула нам пустой масив, регистриуем чат
        if not check_chat:

            #Ответ на клабэк запрос
            bot.answer_callback_query(self.call.id, true_answer)
            #удаляем кнопки
            bot.delete_message(self.call.message.chat.id, self.call.message.message_id)

            return False

        else:

            #Ответ на клабэк запрос
            bot.answer_callback_query(self.call.id, false_answer)
            #удаляем кнопки
            bot.delete_message(self.call.message.chat.id, self.call.message.message_id)
        
            return True

        


