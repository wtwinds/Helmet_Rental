from flask import Flask, render_template, request, redirect, url_for, session, flash
from pymongo import MongoClient
from config import MONGO_URI
import os

app = Flask(__name__)
app.secret_key = "helmet_secret_key"

# MongoDB connection
client = MongoClient(MONGO_URI)
db = client["helmet_rental"]
users = db["users"]
riders=db["rider_info"]

#upload doc
UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Home Page
@app.route("/")
def home():
    return render_template("index.html")


# Login Page
@app.route("/login")
def login():
    return render_template("login.html")


# Register Page
@app.route("/register")
def register():
    return render_template("register.html")


# Register User
@app.route("/submit", methods=["POST"])
def submit():

    name = request.form.get("name")
    email = request.form.get("email").strip().lower()
    phone = request.form.get("phone")
    password = request.form.get("password")

    existing_user = users.find_one({"email": email})

    if existing_user:
        flash("User already registered. Please login.", "warning")
        session["user_name"]=name
        return redirect(url_for("shop"))

    user_data = {
        "name": name,
        "email": email,
        "phone": phone,
        "password": password
    }

    users.insert_one(user_data)

    flash("Registration successful. Please login.", "rigster_success")

    return redirect(url_for("login"))


# Login User
@app.route("/login-user", methods=["POST"])
def login_user():

    email = request.form.get("email").strip().lower()
    password = request.form.get("password")

    user = users.find_one({"email": email})

    if not user:
        flash("Email not registered.", "login_error")
        return redirect(url_for("login"))

    if user["password"] != password:
        flash("Wrong password.", "login_error")
        return redirect(url_for("login"))

    session["user_name"] = user["name"]
    return redirect(url_for("shop"))

#shop select
@app.route("/shop")
def shop():

    if "user_name" not in session:
        return redirect(url_for("login"))

    return render_template("shop_select.html")

#rider-info
@app.route("/rider-info")
def rider_info():

    if "user_name" not in session:
        return redirect(url_for("login"))

    return render_template("rider_info.html")

#save rider info
@app.route("/save-rider", methods=["POST"])
def save_rider():

    fullname = request.form.get("fullname")
    contact = request.form.get("contact")
    id_type = request.form.get("id_type")
    id_number = request.form.get("id_number")
    hotel_name = request.form.get("hotel_name")
    room_no = request.form.get("room_no")
    helmet_count = request.form.get("helmet_count")

    id_file = request.files.get("id_image")

    filename = ""

    if id_file and id_file.filename != "":
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], id_file.filename)
        id_file.save(filepath)
        filename = id_file.filename

    rider_data = {

        "user_name": session["user_name"],
        "fullname": fullname,
        "contact": contact,
        "id_type": id_type,
        "id_number": id_number,
        "hotel_name": hotel_name,
        "room_no": room_no,
        "helmet_count": helmet_count,
        "document_file": filename
    }

    riders.insert_one(rider_data)

    flash("Welcome to Helmet Rental App", "rider_success")

    return redirect(url_for("rider_info"))

# Logout
@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully.", "info")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)