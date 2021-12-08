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


@app.route("/")
@app.route("/get_potholes")
def get_potholes():
    potholes = mongo.db.potholes.find()
    return render_template("potholes.html", potholes=potholes)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if the username already exists in database
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exisits", "flash_error")
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
        flash("Registration successful", "flash_success")

    counties = mongo.db.counties.find().sort("county_name", 1)
    return render_template("register.html", counties=counties)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
