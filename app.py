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
rents = db["rent_duration"]
feedbacks=db["feedback"]

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
    hotel_name = request.form.get("hotel_name")
    room_no = request.form.get("room_no")
    helmet_count = request.form.get("helmet_count")

    session["helmet_count"] = int(helmet_count)
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
        "hotel_name": hotel_name,
        "room_no": room_no,
        "helmet_count": helmet_count,
        "document_file": filename
    }

    riders.insert_one(rider_data)

    flash("Welcome to Helmet Rental App", "rider_success")

    return redirect(url_for("rent_duration"))

# rent duration page
@app.route("/rent-duration")
def rent_duration():

    if "user_name" not in session:
        return redirect(url_for("login"))

    return render_template("rent_duration.html")

@app.route("/save-rent", methods=["POST"])
def save_rent():

    start_day = request.form.get("start_day")
    end_day = request.form.get("end_day")

    # video_file = request.files.get("helmet_video")

    # video_name = ""

    # if video_file and video_file.filename != "":
    #     path = os.path.join(app.config["UPLOAD_FOLDER"], video_file.filename)
    #     video_file.save(path)
    #     video_name = video_file.filename

    rent_data = {
        "user_name": session["user_name"],
        "start_day": start_day,
        "end_day": end_day,
        # "helmet_video": video_name
    }

    rents.insert_one(rent_data)

    flash("Helmet rental verification completed", "success")

    return redirect(url_for("payment"))

#---------Payment--------------------
@app.route("/payment")
def payment():

    if "user_name" not in session:
        return redirect(url_for("login"))

    helmet_count = session.get("helmet_count", 1)

    price_per_helmet = 50

    total_price = helmet_count * price_per_helmet

    return render_template("payment.html",
                           helmet_count=helmet_count,
                           total_price=total_price)

# -------- Booking Complete Page --------
@app.route("/booking-success")
def booking_success():

    if "user_name" not in session:
        return redirect(url_for("login"))

    return render_template("booking_success.html")

#-----Feedback Save----------
@app.route("/save-feedback", methods=["POST"])
def save_feedback():

    rating = request.form.get("rating")
    comment = request.form.get("comment")

    feedback_data = {

        "user_name": session["user_name"],
        "rating": rating,
        "comment": comment
    }

    feedbacks.insert_one(feedback_data)

    flash("Thanks for your feedback!", "success")

    return redirect(url_for("home"))

# Logout
@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully.", "info")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)