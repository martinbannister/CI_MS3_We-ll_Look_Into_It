from itertools import count
import os
import re
from flask import (Flask, flash, render_template, redirect,
                   request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from pymongo.message import query
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


# ---------------------------- DEFAULT / GET POTHOLES -------------------------
@app.route("/")
@app.route("/get_potholes")
def get_potholes():
    potholes = list(mongo.db.potholes.find())
    return render_template("potholes.html", potholes=potholes)


# ---------------------------- POTHOLE SEARCH -------------------------
@app.route("/pothole_search", methods=["GET", "POST"])
def pothole_search():
    search_query = request.form.get("pothole_query")
    potholes = list(mongo.db.potholes.find(
        {"$text": {"$search": search_query}}))
    return render_template("potholes.html", potholes=potholes)


# -----------------------------------------------------------------------
# ---------------------------- USER FEATURES ----------------------------

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


# --------------------------------------------------------------------------
# ---------------------------- POTHOLE FEATURES ----------------------------

# ---------------------------- ADD POTHOLE ----------------------------
@app.route("/add_pothole", methods=["GET", "POST"])
def add_pothole():
    if request.method == "POST":
        pothole = {
            "created_by": session["user"],
            "county_name": request.form.get("county_name"),
            "area_name": request.form.get("area_name"),
            "pothole_location": request.form.get("pothole_location"),
            "depth": int(request.form.get("depth")),
            "photo": request.form.get("photo"),
            "severity": int(request.form.get("severity")),
            "comments": request.form.get("comments"),
            "admin_comments": "",
            "upvotes": 0,
            "read_status": "unread",
            "pothole_status": "Pending"
        }
        mongo.db.potholes.insert_one(pothole)
        flash("Pothole submitted for review", "flash_success")
        return redirect(url_for("get_potholes"))

    counties = mongo.db.counties.find().sort("county_name", 1)
    return render_template("add_pothole.html", counties=counties)


# ---------------------------- EDIT POTHOLE ----------------------------
@app.route("/edit_pothole/<pothole_id>", methods=["GET", "POST"])
def edit_pothole(pothole_id):
    if request.method == "POST":
        submit_pothole = {
            "created_by": session["user"],
            "county_name": request.form.get("county_name"),
            "area_name": request.form.get("area_name"),
            "pothole_location": request.form.get("pothole_location"),
            "depth": int(request.form.get("depth")),
            "photo": request.form.get("photo"),
            "severity": int(request.form.get("severity")),
            "comments": request.form.get("comments")
        }
        mongo.db.potholes.update_one(
            {"_id": ObjectId(pothole_id)}, {"$set": submit_pothole})
        flash("Pothole updated", "flash_success")

    pothole = mongo.db.potholes.find_one({"_id": ObjectId(pothole_id)})
    counties = mongo.db.counties.find().sort("county_name", 1)
    return render_template("edit_pothole.html",
                           pothole=pothole, counties=counties)


# ---------------------------- DELETE POTHOLE ----------------------------
@app.route("/delete_pothole/<pothole_id>")
def delete_pothole(pothole_id):
    mongo.db.potholes.delete_one({"_id": ObjectId(pothole_id)})
    flash("Pothole successfully deleted", "flash_success")
    return redirect(url_for("get_potholes"))


# ---------------------------- UPVOTE ----------------------------
# Allows a user to upvote a pothole
# currently allows multiple votes per user
@app.route("/upvote_pothole/<pothole_id>")
def upvote_pothole(pothole_id):
    pothole = mongo.db.potholes.find_one({"_id": ObjectId(pothole_id)})
    current_votes = pothole['upvotes']
    new_votes = current_votes+1
    update_pothole = {
        "upvotes": new_votes
    }
    mongo.db.potholes.update_one(
        {"_id": ObjectId(pothole_id)}, {"$set": update_pothole})
    flash("Your vote has been registered", "flash_success")
    return redirect(url_for("get_potholes"))


# ---------------------------------------------------------------------------
# ---------------------------- COUNTIES FEATURES ----------------------------

# ---------------------------- GET COUNTIES ----------------------------
@app.route("/get_counties")
def get_counties():
    counties = list(mongo.db.counties.find().sort("county_name", 1))
    return render_template("counties.html", counties=counties)


# ---------------------------- ADD COUNTY ----------------------------
@app.route("/add_county", methods=["GET", "POST"])
def add_county():
    if request.method == "POST":
        county = {
            "county_name": request.form.get("county_name"),
            "primary_colour": request.form.get("primary_colour"),
            "logo_url": request.form.get("logo_url")
        }
        mongo.db.counties.insert_one(county)
        flash("New County Added", "flash_success")
        return redirect(url_for("get_counties"))

    return render_template("add_county.html")


# ---------------------------- EDIT COUNTY ----------------------------
@app.route("/edit_county/<county_id>", methods=["GET", "POST"])
def edit_county(county_id):
    if request.method == "POST":
        submit_county = {
            "county_name": request.form.get("county_name"),
            "primary_colour": request.form.get("primary_colour"),
            "logo_url": request.form.get("logo_url")
        }
        mongo.db.counties.update_one({"_id": ObjectId(
            county_id)}, {"$set": submit_county})
        flash("County successfully updated", "flash_success")
        return redirect(url_for("get_counties"))

    county = mongo.db.counties.find_one({"_id": ObjectId(county_id)})
    return render_template("edit_county.html", county=county)


# ---------------------------- DELETE COUNTY ----------------------------
@app.route("/delete_county/<county_id>")
def delete_county(county_id):
    mongo.db.counties.delete_one({"_id", ObjectId(county_id)})
    flash("County Deleted", "flash_success")
    return redirect(url_for("get_counties"))


# ---------------------------------------------------------------------------
# ---------------------------- AREA FEATURES ----------------------------

# ---------------------------- GET AREAS ----------------------------
@app.route("/get_areas")
def get_areas():
    areas = list(mongo.db.areas.find().sort("county_name", 1))
    return render_template("areas.html", areas=areas)


# ---------------------------- ADD AREA ----------------------------
@app.route("/add_area", methods=["GET", "POST"])
def add_area():
    if request.method == "POST":
        area = {
            "area_name": request.form.get("area_name"),
            "county_name": request.form.get("county_name")
        }
        mongo.db.areas.insert_one(area)
        flash("New Area Added", "flash_success")
        return redirect(url_for("get_areas"))

    # get counties to pass to add area to popuplate counties select
    counties = mongo.db.counties.find().sort("county_name", 1)
    return render_template("add_area.html", counties=counties)


# ---------------------------- EDIT AREA ----------------------------
@app.route("/edit_area/<area_id>", methods=["GET", "POST"])
def edit_area(area_id):
    if request.method == "POST":
        submit_area = {
            "county_name": request.form.get("county_name"),
            "area_name": request.form.get("area_name")
        }
        mongo.db.areas.update_one({"_id": ObjectId(
            area_id)}, {"$set": submit_area})
        flash("Area successfully updated", "flash_success")
        return redirect(url_for("get_areas"))

    area = mongo.db.areas.find_one({"_id": ObjectId(area_id)})
    # get counties to pass to add area to popuplate counties select
    counties = mongo.db.counties.find().sort("county_name", 1)
    return render_template("edit_area.html", area=area, counties=counties)


# ---------------------------- DELETE AREA ----------------------------
@app.route("/delete_area/<area_id>")
def delete_area(area_id):
    mongo.db.areas.delete_one({"_id", ObjectId(area_id)})
    flash("Area Deleted", "flash_success")
    return redirect(url_for("get_areas"))


# ----------------------------  ----------------------------
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
