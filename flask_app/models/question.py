from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_app.models import reply

class Question():
    def __init__(self, data):
        self.id = data['id']
        self.q_text = data['q_text']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def add_question(cls, data):
        query = "INSERT INTO questions (q_text) VALUES (%(q_text)s);"
        return connectToMySQL("xbirthday").query_db(query, data)

    @classmethod
    def delete_question(cls, data):
        query = "DELETE FROM questions WHERE id = %(id)s;"
        return connectToMySQL("xbirthday").query_db(query, data)

    @classmethod
    def edit_question(cls, data):
        query = "UPDATE questions SET q_text = %(q_text)s WHERE id = %(id)s;"
        return connectToMySQL("xbirthday").query_db(query, data)

    @classmethod
    def all_questions(cls):
        query = "SELECT * FROM questions;"
        return connectToMySQL("xbirthday").query_db(query)

    @classmethod
    def all_qs_res(cls):
        query = "SELECT * FROM questions LEFT JOIN replies ON questions.id = replies.question_id;"
        results = connectToMySQL("xbirthday").query_db(query)
        replies = []
        if results:
            for row in results:
                temp_reply = cls(row)
                reply_data = {
                    "id": row["replies.id"],
                    "r_text": row["r_text"],
                    "user_id": row["user_id"],
                    "question_id" : row["question_id"]
                }
                temp_reply.maker = reply.Reply(reply_data)
                replies.append(temp_reply)
        return replies