from .database import App_Db


#Клас содержащий в себе все базовые методы для работы приложения
class Core_Methods:

    def __init__(self, target, data):

        self.target = target
        self.data = data

    #Возвращает объект по его ID, если он есть в БД
    def check_obj(self):

        db  = App_Db()

        if self.target == "chat":

            res = db.get_chat(self.data)
            return res

        elif self.target == "user":

            res = db.get_user(self.data)
            return res
            

    #Регистрирует объект в БД      
    def reg_obj(self, reg_object):

        db = App_Db()

        if self.target == "chat":

            clan = (reg_object)
            db.clan_registration(clan)

        elif self.target == "user":

            user = (reg_object)
            db.user_registration(user)


    #Удаляем объект из БД
    def del_obj(self):
        
        db = App_Db()
        
        if self.target == "chat":

            db.delete_clan(self.data)

        elif self.target == "user":

            db.delete_user(self.data)



class Clans:

    def __init__(self, chat_id):
        
        self.chat_id = chat_id


    def get_active_status(self):

        db = App_Db()
        res = db.get_chat(self.chat_id)

        return res[0][4]


    def active_status_change(self, status):

        db = App_Db()
        up_status = [status, self.chat_id]
        db.update_status_clan(up_status)



class Users:

    def __init__(self, user_id):
        
        self.user_id = user_id

