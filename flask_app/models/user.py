from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_bcrypt import Bcrypt
from flask import flash
bcrypt=Bcrypt(app)


class User():
    def __init__(self, data):
        self.id = data['id']
        self.username = data['username']
        self.password = data['password']


    @classmethod
    def create_user(cls, data):
        hash_browns = bcrypt.generate_password_hash(data["password"])
        hashed_dict = {
            "username" : data["username"],
            "password" : hash_browns
        }
        query = "INSERT INTO users (username, password) VALUES (%(username)s, %(password)s);"
        return connectToMySQL("xbirthday").query_db(query, hashed_dict)

    @classmethod
    def get_by_user(cls, data):
        query = "SELECT * FROM users WHERE username = %(username)s;"
        result = connectToMySQL("xbirthday").query_db(query, data)
        if result:
            return cls(result[0])


    @staticmethod
    def validate_user(data):
        is_valid=True
        if data['username'] == "":
            flash("Please enter a username")
            is_valid = False
        if len(data['username']) < 4:
            flash("Username must be at least 5 characters long!")
            is_valid = False
        check = User.get_by_user(data['username'])
        if check:
            flash("Username already in use!")
            is_valid = False
        if data['password'] == "":
            flash("Please enter a password")
            is_valid = False
        if len(data['password']) < 8:
            flash("Password must be 8 characters long")
            is_valid = False
        if data['password'] != data['conf_password']:
            flash("Passwords must match!")
            is_valid = False
        return is_valid