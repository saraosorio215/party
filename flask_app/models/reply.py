from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app

class Reply():
    def __init__(self, data):
        self.id = data['id']
        self.r_text = data['r_text']
        self.user_id = data['user_id']
        self.question_id = data['question_id']


    @classmethod
    def add_reply(cls, data):
        query = "INSERT INTO replies (r_text, question_id, user_id) VALUES (%(r_text)s, %(question_id)s, %(user_id)s);"
        return connectToMySQL("xbirthday").query_db(query, data)

    @classmethod
    def update_reply(cls, data):
        query = "UPDATE replies SET r_text = %(r_text)s WHERE id = %(id)s;"
        return connectToMySQL("xbirthday").query_db(query, data)

    @classmethod
    def delete_reply(cls, data):
        query = "DELETE FROM replies WHERE id = %(id)s;"
        return connectToMySQL("xbirthday").query_db(query, data)