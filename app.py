import os
from flask import (Flask, flash, render_template, redirect,
                   request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import pymongo
from pymongo.message import query
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


# CUSTOM ERROR PAGES
# REFERENCE: Grinberg (2018) Flask Web Development - See README.md
# ---------------------------- CUSTOM 404 PAGE -------------------------
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


# ---------------------------- CUSTOM 500 PAGE -------------------------
@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500


# ---------------------------- DEFAULT / GET REPORTS -------------------------
@app.route("/")
@app.route("/get_reports")
def get_reports():
    reports = list(mongo.db.reports.find())
    return render_template("reports.html", reports=reports)


# ---------------------------- REPORT SEARCH -------------------------
@app.route("/report_search", methods=["GET", "POST"])
def report_search():
    search_query = request.form.get("report_query")
    reports = list(mongo.db.reports.find(
        {"$text": {"$search": search_query}}))
    return render_template("reports.html", reports=reports)


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
            "fullname": request.form.get("fullname"),
            "email": request.form.get("email"),
            "password": generate_password_hash(request.form.get("password")),
            "primary_county": request.form.get("primary_county"),
            "admin": False,
            "master_admin": False
        }
        mongo.db.users.insert_one(register)

        # put the new user into 'session' cookie & default to non-admin
        session["user"] = request.form.get("username").lower()
        session["admin"] = False
        session["master_admin"] = False
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
                session["master_admin"] = existing_user["master_admin"]
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
@app.route("/profile/", methods=["GET", "POST"])
def profile():

    if session.get("user"):
        # if there is a logged in user retrieve their reports
        if session["user"]:
            # get the session users username & fullname from the database
            user = mongo.db.users.find_one({"username": session["user"]},
                                           ["username", "fullname"])
            users_reports = mongo.db.reports.find(
                                            {"created_by": user["username"]})
            # pass user dictionary and user reports to profile page
            return render_template("profile.html", user=user,
                                   users_reports=users_reports)

    return redirect(url_for("login"))


# ---------------------------- LOGOUT ----------------------------
@app.route("/logout")
def logout():
    flash("You have successfully logged out", "flash_info")
    session.pop("user")
    session.pop("admin")
    session.pop("master_admin")
    return redirect(url_for("login"))


# ---------------------------- USER MANAGEMENT ----------------------------
@app.route("/users")
@app.route("/users/<user_id>")
def users(user_id=None):
    if user_id:
        cur_user = mongo.db.users.find_one({"_id": ObjectId(user_id)},
                                           ["fullname",
                                            "admin",
                                            "master_admin"])
    session_user = mongo.db.users.find_one({"username": session["user"]},
                                           ["master_admin"])
    users = list(mongo.db.users.find().sort([
                                             ("primary_county",
                                              pymongo.ASCENDING),
                                             ("fullname",
                                              pymongo.ASCENDING)]))
    counties = list(mongo.db.counties.find().sort("county_name",
                                                  pymongo.ASCENDING))
    return render_template("users.html",
                           users=users,
                           counties=counties,
                           session_user=session_user,
                           cur_user=cur_user if user_id else None)


# ---------------------------- UPDATE USER ----------------------------
@app.route("/update_user/<user_id>", methods=["GET", "POST"])
def update_user(user_id=None):
    is_admin = True if request.form.get("is_admin") else False
    is_master_admin = True if request.form.get("is_master_admin") else False
    if request.method == "POST":
        submit_user = {
            "admin": is_admin,
            "master_admin": is_master_admin
        }
        mongo.db.users.update_one(
            {"_id": ObjectId(user_id)}, {"$set": submit_user})
        flash("User successfully updated", "flash_success")

    return users(user_id)


# --------------------------------------------------------------------------
# ---------------------------- REPORT FEATURES ----------------------------

# ---------------------------- ADD REPORT ----------------------------
@app.route("/add_report", methods=["GET", "POST"])
def add_report():
    if request.method == "POST":
        report = {
            "created_by": session["user"],
            "county_name": request.form.get("county_name"),
            "area_name": request.form.get("area_name"),
            "report_location": request.form.get("report_location"),
            "depth": int(request.form.get("depth")),
            "photo": request.form.get("photo"),
            "severity": int(request.form.get("severity")),
            "comments": request.form.get("comments"),
            "admin_comments": "",
            "upvotes": 0,
            "read_status": "unread",
            "report_status": "Pending"
        }
        mongo.db.reports.insert_one(report)
        flash("report submitted for review", "flash_success")
        return redirect(url_for("get_reports"))

    counties = list(mongo.db.counties.find().sort("county_name", 1))
    areas = list(mongo.db.areas.find().sort([
        ("county_name", pymongo.ASCENDING),
        ("area_name", pymongo.ASCENDING)]))
    return render_template("add_report.html", counties=counties, areas=areas)


# ---------------------------- EDIT REPORT ----------------------------
@app.route("/edit_report/<report_id>", methods=["GET", "POST"])
def edit_report(report_id):
    if request.method == "POST":
        submit_report = {
            "created_by": session["user"],
            "county_name": request.form.get("county_name"),
            "area_name": request.form.get("area_name"),
            "report_location": request.form.get("report_location"),
            "depth": int(request.form.get("depth")),
            "photo": request.form.get("photo"),
            "severity": int(request.form.get("severity")),
            "comments": request.form.get("comments"),
            "read_status": "unread"
        }
        mongo.db.reports.update_one(
            {"_id": ObjectId(report_id)}, {"$set": submit_report})
        flash("report updated", "flash_success")

    report = mongo.db.reports.find_one({"_id": ObjectId(report_id)})
    counties = mongo.db.counties.find().sort("county_name", 1)
    return render_template("edit_report.html",
                           report=report, counties=counties)


# ---------------------------- MANAGE REPORT ----------------------------
@app.route("/manage_report/<report_id>", methods=["GET", "POST"])
def manage_report(report_id):
    if request.method == "POST":
        submit_report = {
            "report_status": request.form.get("report_status"),
            "admin_comments": request.form.get("admin_comments")
        }
        mongo.db.reports.update_one(
            {"_id": ObjectId(report_id)}, {"$set": submit_report})
        flash("Report updated", "flash_success")
    elif request.method == "GET":
        # mark report as read when it's opened
        mongo.db.reports.update_one(
            {"_id": ObjectId(report_id)}, {"$set": {"read_status": "read"}})

    statuses = mongo.db.report_statuses.find().sort(
        "report_status", pymongo.ASCENDING)
    report = mongo.db.reports.find_one({"_id": ObjectId(report_id)})
    return render_template("manage_report.html",
                           report=report, statuses=statuses)


# ---------------------------- DELETE REPORT ----------------------------
@app.route("/delete_report/<report_id>")
def delete_report(report_id):
    mongo.db.reports.delete_one({"_id": ObjectId(report_id)})
    flash("Report successfully deleted", "flash_success")
    return redirect(url_for("get_reports"))


# ---------------------------- UPVOTE ----------------------------
# Allows a user to upvote a report
# currently allows multiple votes per user
@app.route("/upvote_report/<report_id>")
def upvote_report(report_id):
    report = mongo.db.reports.find_one({"_id": ObjectId(report_id)})
    current_votes = report['upvotes']
    new_votes = current_votes+1
    update_report = {
        "upvotes": new_votes
    }
    mongo.db.reports.update_one(
        {"_id": ObjectId(report_id)}, {"$set": update_report})
    flash("Your vote has been registered", "flash_success")
    return redirect(url_for("get_reports"))


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
        # check if user is authorised to do this
        if session["master_admin"]:
            county = {
                "county_name": request.form.get("county_name"),
                "primary_colour": request.form.get("primary_colour"),
                "logo_url": request.form.get("logo_url")
            }
            mongo.db.counties.insert_one(county)
            flash("New County Added", "flash_success")
            return redirect(url_for("get_counties"))

    if session["master_admin"]:
        return render_template("add_county.html")
    else:
        flash("You are not authorised to access this page", "flash_error")
        return redirect(url_for("get_reports"))


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
    mongo.db.counties.delete_one({"_id": ObjectId(county_id)})
    flash("County Deleted", "flash_success")
    return redirect(url_for("get_counties"))


# ---------------------------------------------------------------------------
# ---------------------------- AREA FEATURES ----------------------------

# ---------------------------- GET AREAS ----------------------------
@app.route("/get_areas")
def get_areas():
    if session.get("admin"):
        if session["admin"]:
            areas = list(mongo.db.areas.find().sort("county_name", 1))
            return render_template("areas.html", areas=areas)
    else:
        flash("You are not authorised to access this page", "flash_error")
        return redirect(url_for("get_potholes"))


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
    mongo.db.areas.delete_one({"_id": ObjectId(area_id)})
    flash("Area Deleted", "flash_success")
    return redirect(url_for("get_areas"))


# ---------------------------------------------------------------------------
# ---------------------------- STATUS FEATURES ----------------------------

# ---------------------------- GET STATUS' ----------------------------
@app.route("/get_status")
def get_status():
    statuses = list(mongo.db.pothole_statuses.find().sort("pothole_status", 1))
    return render_template("ph_status.html", statuses=statuses)


# ---------------------------- ADD STATUS ----------------------------
@app.route("/add_status", methods=["GET", "POST"])
def add_status():
    if request.method == "POST":
        status = {
            "pothole_status": request.form.get("pothole_status")
        }
        mongo.db.pothole_statuses.insert_one(status)
        flash("New Status Added", "flash_success")
        return redirect(url_for("get_status"))

    return render_template("add_status.html")


# ---------------------------- EDIT STATUS ----------------------------
@app.route("/edit_status/<status_id>", methods=["GET", "POST"])
def edit_status(status_id):
    if request.method == "POST":
        submit_status = {
            "pothole_status": request.form.get("pothole_status")
        }
        mongo.db.pothole_statuses.update_one({"_id": ObjectId(
            status_id)}, {"$set": submit_status})
        flash("Status successfully updated", "flash_success")
        return redirect(url_for("get_status"))

    status = mongo.db.pothole_statuses.find_one({"_id": ObjectId(status_id)})
    return render_template("edit_status.html", status=status)


# ---------------------------- DELETE STATUS ----------------------------
@app.route("/delete_status/<status_id>")
def delete_status(status_id):
    mongo.db.pothole_statuses.delete_one({"_id": ObjectId(status_id)})
    flash("Status Deleted", "flash_success")
    return redirect(url_for("get_status"))


# ----------------------------  ----------------------------
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=False)
