from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash

class Reservation():
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.num_adults = data['num_adults']
        self.num_kids = data['num_kids']
        self.kidname_1 = data["kidname_1"]
        self.kidname_2 = data["kidname_2"]
        self.kidname_3 = data["kidname_3"]
        self.kidname_4 = data["kidname_4"]
        self.kidsize_1 = data["kidsize_1"]
        self.kidsize_2 = data["kidsize_2"]
        self.kidsize_3 = data["kidsize_3"]
        self.kidsize_4 = data["kidsize_4"]
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def get_all_res(cls):
        query = "SELECT * FROM reservations ORDER BY name ASC;"
        return connectToMySQL("xbirthday").query_db(query)

    @classmethod
    def get_kid_names(cls):
        query = "SELECT * FROM reservations;"
        result = connectToMySQL("xbirthday").query_db(query)
        allKids = []
        for i in result:
            if i["kidname_1"] != "":
                allKids.append(i["kidname_1"] + " : " + i["kidsize_1"])
            if i["kidname_2"] != "":
                allKids.append(i["kidname_2"] + " : " + i["kidsize_2"])
            if i["kidname_3"] != "":
                allKids.append(i["kidname_3"] + " : " + i["kidsize_3"])
            if i["kidname_4"] != "":
                allKids.append(i["kidname_4"] + " : " + i["kidsize_4"])
        allKids.sort()
        return allKids

    @classmethod
    def get_kid_total(cls):
        query = "SELECT * FROM reservations;"
        result = connectToMySQL("xbirthday").query_db(query)
        count = 0
        for i in result:
            count += i["num_kids"]
        return count

    @classmethod
    def get_adult_total(cls):
        query = "SELECT * FROM reservations;"
        result = connectToMySQL("xbirthday").query_db(query)
        count = 0
        for i in result:
            count += i["num_adults"]
        return count

    @classmethod
    def get_res_byid(cls, data):
        query = "SELECT * FROM reservations WHERE id = %(id)s;"
        result = connectToMySQL("xbirthday").query_db(query, data)
        if result:
            return cls(result[0])

    @classmethod
    def add_res(cls, data):
        query = "INSERT INTO reservations (name, num_adults, num_kids, kidname_1, kidname_2, kidname_3, kidname_4, kidsize_1, kidsize_2, kidsize_3, kidsize_4) VALUES (%(name)s, %(num_adults)s, %(num_kids)s, %(kidname_1)s, %(kidname_2)s, %(kidname_3)s, %(kidname_4)s, %(kidsize_1)s, %(kidsize_2)s, %(kidsize_3)s, %(kidsize_4)s);"
        return connectToMySQL("xbirthday").query_db(query, data)

    @classmethod
    def delete_res(cls, data):
        query = "DELETE FROM reservations WHERE id = %(id)s;"
        return connectToMySQL("xbirthday").query_db(query, data)

    @staticmethod
    def validate_class(data):
        is_valid = True
        if len(data["name"]) <=1:
            is_valid = False
            flash("Enter name | Entre nombre")
        if (data["num_kids"]) == '':
            is_valid = False
            flash("Enter number of kids | Entre numero de niños")
        if (data["num_adults"]) == '':
            is_valid = False
            flash("Enter number of adults | Entre numero de adultos")
        return is_valid