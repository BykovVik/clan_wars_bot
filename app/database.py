import mysql.connector as connector
from config import DB_CONFIG

class App_Db:

    def __init__(self):
        
        try:

            self.conn = connector.connect(host=DB_CONFIG[0], database=DB_CONFIG[1], user=DB_CONFIG[2], password=DB_CONFIG[3])
            self.cursor = self.conn.cursor()

            if self.conn.is_connected():
                print("Соединение с БД установлено")

        except connector.Error as e:

            print(e)
            print("Ошибка подключения к Базе Данных")

    

    def clan_registration(self, new_chat):

        self.cursor.execute("INSERT INTO clans(chat_name, chat_id, chat_item, chat_active) VALUES(%s, %s, %s, %s)", new_chat)
        self.conn.commit()
        self.conn.close()



    def update_status_clan(self, up_clan):

        self.cursor.execute("UPDATE clans SET chat_active=%s WHERE chat_id=%s", (up_clan))
        self.conn.commit()



    def delete_clan(self, chat_id):

        self.cursor.execute("DELETE FROM clans WHERE chat_id={}".format(str(chat_id)))
        self.conn.commit()
        self.conn.close()



    def get_chat(self, chat_id):

        self.cursor.execute("SELECT id, chat_name, chat_id, chat_item, chat_active FROM clans WHERE chat_id={}".format(str(chat_id)))
        res = self.cursor.fetchall()
        self.conn.close()

        return res


    def user_registration(self, new_user):

        self.cursor.execute("INSERT INTO users(username, user_id, user_item, captcha_active, captcha_error, users_clan) VALUES(%s, %s, %s, %s, %s, %s)", new_user)
        self.conn.commit()
        self.conn.close()


    def update_status_captcha(self, up_captcha):

        self.cursor.execute("UPDATE users SET captcha_active=%s WHERE user_id=%s", (up_captcha))
        self.conn.commit()


    def update_sum_captcha_error(self, up_captcha_error):

        self.cursor.execute("UPDATE users SET captcha_error=%s WHERE user_id=%s", (up_captcha_error))
        self.conn.commit()


    def update_user_item(self, up_item):

        self.cursor.execute("UPDATE users SET user_item=%s WHERE user_id=%s", (up_item))
        self.conn.commit()


    def get_user(self, user_id):

        self.cursor.execute("SELECT id, username, user_id, user_item, captcha_active, captcha_error, users_clan FROM users WHERE user_id={}".format(str(user_id)))
        res = self.cursor.fetchall()
        self.conn.close()

        return res


    def delete_user(self, user_id):

        self.cursor.execute("DELETE FROM users WHERE user_id={}".format(str(user_id)))
        self.conn.commit()
        self.conn.close()
            