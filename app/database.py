from app.db import clan, user
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

        up = clan.update().where(
            clan.c.chat_id == up_clan[1]
        ).values(
            chat_active = up_clan[0]
        )

        conn = db_engine.connect()
        conn.execute(up)


    def delete_clan(self, chat_id):

        del_obj = delete(clan).where(
            clan.c.chat_id == chat_id
        )

        conn = db_engine.connect()
        conn.execute(del_obj)


    def user_registration(self, new_user):

        insert = user.insert().values(
            
            user_activation = new_user[0],
            username = new_user[1],
            user_id = new_user[2],
            user_item = new_user[3],
            captcha_active = new_user[4],
            captcha_error = new_user[5],
            users_clan = new_user[6],
        )

        conn = db_engine.connect()
        conn.execute(insert)


    def update_status_captcha(self, up_captcha):

        self.cursor.execute("UPDATE users SET captcha_active=%s WHERE user_id=%s", (up_captcha))
        self.conn.commit()


    def update_sum_captcha_error(self, up_captcha_error):

        self.cursor.execute("UPDATE users SET captcha_error=%s WHERE user_id=%s", (up_captcha_error))
        self.conn.commit()


    def update_user_item(self, up_item):

        self.cursor.execute("UPDATE users SET user_item=%s WHERE user_id=%s", (up_item))
        self.conn.commit()


    def activation_user(self, up_item):

        self.cursor.execute("UPDATE users SET user_activation=%s WHERE user_id=%s", (up_item))
        self.conn.commit()


    def get_user(self, user_id):

        self.cursor.execute("SELECT id, user_activation, username, user_id, user_item, captcha_active, captcha_error, users_clan FROM users WHERE user_id={}".format(str(user_id)))
        res = self.cursor.fetchall()
        self.conn.close()

        return res


    def delete_user(self, user_id):

        self.cursor.execute("DELETE FROM users WHERE user_id={}".format(str(user_id)))
        self.conn.commit()
        self.conn.close()
            