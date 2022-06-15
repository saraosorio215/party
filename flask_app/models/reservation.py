from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app

class Reservation():
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.num_adults = data['num_adults']
        self.num_kids = data['num_kids']
        self.kid_1 = data["kid_1"]
        self.kid_2 = data["kid_2"]
        self.kid_3 = data["kid_3"]
        self.kid_4 = data["kid_4"]
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
            if i["kid_1"] != "":
                allKids.append(i["kid_1"])
            if i["kid_2"] != "":
                allKids.append(i["kid_2"])
            if i["kid_3"] != "":
                allKids.append(i["kid_3"])
            if i["kid_4"] != "":
                allKids.append(i["kid_4"])
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
        query = "INSERT INTO reservations (name, num_adults, num_kids, kid_1, kid_2, kid_3, kid_4) VALUES (%(name)s, %(num_adults)s, %(num_kids)s, %(kid_1)s, %(kid_2)s, %(kid_3)s, %(kid_4)s);"
        return connectToMySQL("xbirthday").query_db(query, data)

    @classmethod
    def delete_res(cls, data):
        query = "DELETE FROM reservations WHERE id = %(id)s;"
        return connectToMySQL("xbirthday").query_db(query, data)