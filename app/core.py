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