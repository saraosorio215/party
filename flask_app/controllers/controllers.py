from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import question, reply, reservation, user
from flask_bcrypt import Bcrypt
bcrypt=Bcrypt(app)

#*---------------------------------DISPLAY ROUTES-------------------------------------

@app.route("/")
def main_page():
    all_questions = question.Question.all_qs_res()
    return render_template("index.html", all_questions = all_questions)

@app.route("/reserved/")
def reserved():
    return render_template("reserved.html")

@app.route("/login/")
def login():
    return render_template("login.html")

@app.route("/dashboard/")
def dashboard():
    if "user_id" in session:
        all_resv = reservation.Reservation.get_all_res()
        all_questions = question.Question.all_qs_res()
        all_names = reservation.Reservation.get_kid_names()
        kid_total = reservation.Reservation.get_kid_total()
        adult_total = reservation.Reservation.get_adult_total()
        return render_template("dashboard.html", all_resv = all_resv, all_questions = all_questions, all_names = all_names, kid_total = kid_total, adult_total = adult_total)
    return("/login/")

@app.route("/logout/")
def logout():
    session.clear()
    return redirect("/login/")


#*----------------------------------ACTION ROUTES-------------------------------------

@app.route("/new/rsvp/", methods=['POST'])
def newRsvp():
    if reservation.Reservation.validate_class(request.form):
        data = {
            "name" : request.form["name"],
            "num_kids" : request.form["num_kids"],
            "num_adults" : request.form["num_adults"],
            "kidname_1" : request.form["kidname_1"],
            "kidname_2" : request.form["kidname_2"],
            "kidname_3" : request.form["kidname_3"],
            "kidname_4" : request.form["kidname_4"],
            "kidsize_1" : request.form["kidsize_1"],
            "kidsize_2" : request.form["kidsize_2"],
            "kidsize_3" : request.form["kidsize_3"],
            "kidsize_4" : request.form["kidsize_4"]
        }
        reservation.Reservation.add_res(data)
        return redirect("/reserved/")
    return redirect("/")

@app.route("/new/question/", methods=['POST'])
def newQ():
    data = {
        "q_text" : request.form["q_text"]
    }
    question.Question.add_question(data)
    return redirect("/")

@app.route("/new/reply/", methods=['POST'])
def newRes():
    data = {
        "r_text" : request.form["r_text"],
        "question_id" : request.form["question_id"],
        "user_id" : session["user_id"]
    }
    reply.Reply.add_reply(data)
    return redirect("/dashboard/")

@app.route("/user/register/", methods=['POST'])
def newUser():
    data = {
        "username" : request.form["username"],
        "password" : request.form["password"],
        "conf_password" : request.form["conf_password"]
    }
    if user.User.validate_user(data):
        person = user.User.create_user(data)
        session["user_id"] = person
        return redirect("/dashboard/")
    return redirect("/")

@app.route("/user/login/", methods=['POST'])
def loginUser():
    data = {
        "username": request.form["username"],
        "password" : request.form["password"]
        }
    user_data = {"username" : request.form["username"]}
    person = user.User.get_by_user(user_data)
    if not person:
        flash("Invalid Username!")
        return redirect("/login/")
    if not bcrypt.check_password_hash(person.password, data['password']):
        flash("Invalid Login!")
        return redirect("/login/") 
    session["user_id"]= person.id
    return redirect("/dashboard/")

@app.route("/delete/q/<int:id>/")
def deleteQ(id):
    data = {"id" : id}
    question.Question.delete_question(data)
    return redirect("/dashboard/")

@app.route("/edit/r/<int:id>/")
def editR(id):
    data = {"id" : id}
    reply.Reply.find_reply(data)
    return render_template("editreply.html")

@app.route("/delete/r/<int:id>/")
def deleteR(id):
    data = {"id" : id}
    reply.Reply.delete_reply(data)
    return redirect("/dashboard/")