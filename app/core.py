from re import A
from .database import App_Db


#Клас содержащий в себе все базовые методы для работы приложения
class Core_Methods:

    def __init__(self, data):

        self.user_id = data.from_user.id
        self.user_name = data.from_user.first_name
        self.chat_id = data.chat.id
        self.chat_title = data.chat.title

    #Возвращает user_id
    def get_user_id(self):

        return self.user_id

    #Возвращает chat_id
    def get_chat_id(self):

        return self.chat_id

    #Возвращает user_name
    def get_user_name(self):

        return self.user_name

    #Возвращает chat_name
    def get_chat_title(self):

        return self.chat_title

    #Возвращает объект user, если он есть в БД
    def check_players(self):

        db  = App_Db()
        res = db.get_user(self.user_id)
        return res

    #Возвращает объект clan, если он есть в БД
    def check_chats(self):

        db  = App_Db()
        res = db.get_chat(self.chat_id)
        return res



#Класс для обработки объектов user
class Player_Stats(Core_Methods):

    def __init__(self, data):

        super().__init__(data)

    def get_player_stat(self):

        status = self.check_players()

        return status

    def reg_user(self, new_user):

        db = App_Db()
        user = (new_user)
        db.user_registration(user)

    def del_user(self):

        db = App_Db()
        db.delete_user(self.user_id)



#Класс для обработки объектов clan
class Clan_Stats(Core_Methods):

    def __init__(self, data):
        super().__init__(data)

    def get_chat_stat(self):

        status = self.check_chats()
        return status

    def reg_clan(self):

        db = App_Db()
        new_chat = ([self.chat_title, self.chat_id, 0])
        db.clan_registration(new_chat)

    def del_clan(self):

        db = App_Db()
        db.delete_clan(self.chat_id)