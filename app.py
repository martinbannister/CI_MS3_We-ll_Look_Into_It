import os
from flask import (Flask, flash, render_template, redirect,
                   request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


# ---------------------------- DEFAULT / GET POTHOLES ----------------------------
@app.route("/")
@app.route("/get_potholes")
def get_potholes():
    potholes = list(mongo.db.potholes.find())
    return render_template("potholes.html", potholes=potholes)


# ---------------------------- REGISTER ----------------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if the username already exists in database
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Sorry, that username already exisits.", "flash_error")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password")),
            "primary_county": request.form.get("primary_county"),
            "admin": False
        }
        mongo.db.users.insert_one(register)

        # put the new users into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("You have successfully registered", "flash_success")
        return redirect(url_for("profile", username=session["user"]))

    counties = mongo.db.counties.find().sort("county_name", 1)
    return render_template("register.html", counties=counties)


# ---------------------------- LOGIN ----------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username exists in database
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                session["admin"] = existing_user["admin"]
                flash("Welcome, {}".format(request.form.get("username")
                                           .capitalize()), "flash_success")
                return redirect(url_for("profile", username=session["user"]))
            else:
                # invalid password
                flash("Incorrect Username and/or Password", "flash_error")
                return redirect(url_for("login"))
        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password", "flash_error")
            return redirect(url_for("login"))

    return render_template("login.html")


# ---------------------------- PROFILE PAGE ----------------------------
@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # get the session users username from the database
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]

    if session["user"]:
        return render_template("profile.html", username=username)

    return redirect(url_for("login"))


# ---------------------------- LOGOUT ----------------------------
@app.route("/logout")
def logout():
    flash("You have successfully logged out", "flash_info")
    session.pop("user")
    return redirect(url_for("login"))


# ---------------------------- ADD POTHOLE ----------------------------
@app.route("/add_pothole")
def add_pothole():
    return render_template("add_pothole.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
