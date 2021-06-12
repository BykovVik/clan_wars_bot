from app.db_table import clan, user
from sqlalchemy import update, delete, select
from app.config import db_engine

class App_Db:

    def clan_registration(self, new_chat):

        insert = clan.insert().values(
            chat_name = new_chat[0],
            chat_id = new_chat[1],
            chat_item = new_chat[2],
            chat_active = new_chat[3],
        )

        conn = db_engine.connect()
        conn.execute(insert)


    def get_chat(self, chat_id):

        select = clan.select().where(clan.c.chat_id == chat_id)

        conn = db_engine.connect()
        res = conn.execute(select)

        return res.fetchall()


    def update_status_clan(self, up_clan):

        up_clan_status = clan.update().where(
            clan.c.chat_id == up_clan[1]
        ).values(
            chat_active = up_clan[0]
        )

        conn = db_engine.connect()
        conn.execute(up_clan_status)


    def delete_clan(self, chat_id):

        del_obj = delete(clan).where(
            clan.c.chat_id == chat_id
        )

        conn = db_engine.connect()
        conn.execute(del_obj)


    def user_registration(self, new_user):

        insert_user = user.insert().values(
            
            user_activation = new_user[0],
            username = new_user[1],
            user_id = new_user[2],
            user_item = new_user[3],
            captcha_active = new_user[4],
            captcha_error = new_user[5],
            users_clan = new_user[6],
        )

        conn = db_engine.connect()
        conn.execute(insert_user)

     
    def update_status_captcha(self, up_captcha):

        print("ЧТО ПРИШЛО", up_captcha)

        up_captcha_stat = user.update().where(
            user.c.user_id == up_captcha[1]
        ).values(
            captcha_active = up_captcha[0]
        )

        conn = db_engine.connect()
        conn.execute(up_captcha_stat)


    def update_sum_captcha_error(self, up_captcha_error):

        up = user.update().where(
            user.c.user_id == up_captcha_error[1]
        ).values(
            captcha_error = up_captcha_error[0]
        )

        conn = db_engine.connect()
        conn.execute(up)


    def update_user_item(self, up_item):

        up = user.update().where(
            user.c.user_id == up_item[1]
        ).values(
            user_item = up_item[0]
        )

        conn = db_engine.connect()
        conn.execute(up)


    def activation_user(self, up_active):

        up = user.update().where(
            user.c.user_id == up_active[1]
        ).values(
            user_activation = up_active[0]
        )

        conn = db_engine.connect()
        conn.execute(up)


    def get_user(self, user_id):

        select = user.select().where(user.c.user_id == user_id)

        conn = db_engine.connect()
        res = conn.execute(select)

        return res.fetchall()


    def delete_user(self, user_id):

        del_obj = delete(user).where(
            user.c.user_id == user_id
        )

        conn = db_engine.connect()
        conn.execute(del_obj)

            