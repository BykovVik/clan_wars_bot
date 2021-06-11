from app.database import App_Db
import random
from app.config import AUDIO_PATH, IMG_PATH


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

    def active_captcha_change(self, captcha_status):

        db = App_Db()
        up_status = [captcha_status, self.user_id]
        db.update_status_captcha(up_status)

    def captcha_error_change(self, error_status):

        db = App_Db()
        up_status = [error_status, self.user_id]
        db.update_sum_captcha_error(up_status)

    def get_sum_captcha_error(self):

        db = App_Db()
        res = db.get_user(self.user_id)

        return res[0][5]

    def update_items(self, update_item):

        db = App_Db()
        up_status = [update_item, self.user_id]
        db.update_user_item(up_status)

    def user_activation(self):

        db = App_Db()
        up_status = [1, self.user_id]
        db.activation_user(up_status)





class Captcha():

    def __init__(self, user_id):

        self.user_id = user_id
        self.audio_path = [
            AUDIO_PATH + '9.ogg',
            AUDIO_PATH + '17.ogg',
            AUDIO_PATH + '18.ogg',
            AUDIO_PATH + '36.ogg',
            AUDIO_PATH + '45.ogg',
            AUDIO_PATH + '365.ogg',
            AUDIO_PATH + '763.ogg',
            AUDIO_PATH + '906.ogg'
        ]

    
    def get_captcha_construct(self):

        random_audio_path = random.choice(self.audio_path)

        true_variant = random_audio_path.split(AUDIO_PATH)[1].split('.')[0]

        audio_pack = [str(random_audio_path), true_variant]

        while len(audio_pack) != 5:

            num = random.randint(1, 999)

            if num != true_variant:

                audio_pack.append(num)

        return audio_pack

