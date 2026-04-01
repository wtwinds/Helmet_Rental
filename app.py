from flask import Flask, render_template, request, redirect, url_for, session, flash
from pymongo import MongoClient
from config import MONGO_URI
from datetime import datetime, date
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
    security_question = request.form.get("security_question")
    security_answer = request.form.get("security_answer").lower()

    existing_user = users.find_one({"email": email})

    if existing_user:
        flash("User already registered. Please login.", "warning")
        session["user_name"]=name
        return redirect(url_for("shop"))

    user_data = {
        "name": name,
        "email": email,
        "phone": phone,
        "password": password,
        "security_question": security_question,
        "security_answer": security_answer
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

    return render_template("shop_select.html", back_url="/login")

#rider-info
@app.route("/rider-info")
def rider_info():

    if "user_name" not in session:
        return redirect(url_for("login"))

    return render_template("rider_info.html", back_url="/shop")

#save rider info
@app.route("/save-rider", methods=["POST"])
def save_rider():

    fullname = request.form.get("fullname")
    contact = request.form.get("contact")
    id_type = request.form.get("id_type")
    hotel_name = request.form.get("hotel_name")
    room_no = request.form.get("room_no")

    normal_helmet = int(request.form.get("normal_helmet",0))
    bluetooth_helmet=int(request.form.get("bluetooth_helmet",0))
    hud_helmet=int(request.form.get("hud_helmet",0))
    
    damage_protection=request.form.get("damage_protection")

    if normal_helmet==0 and bluetooth_helmet==0 and hud_helmet==0:
        flash("Please select at least one helmet", "error")
        return redirect(url_for("rider_info"))
    
    #total_helmets=normal_helmet+bluetooth_helmet+hud_helmet

    if normal_helmet>0 and (bluetooth_helmet>0 or hud_helmet>0):
        flash("Select either Normal or Smart helmets only","error")
        return redirect(url_for("rider_info"))
    
    if normal_helmet>2:
        flash("Maximum 2 Normal helmets allowed", "error")
        return redirect(url_for("rider_info"))
    
    if(bluetooth_helmet+hud_helmet)>2:
        flash("Maximum 2 Smart helmets allowed","error")
        return redirect(url_for("rider_info"))
    
    session["normal_helmet"] = int(normal_helmet)
    session["bluetooth_helmet"]=bluetooth_helmet
    session["hud_helmet"]=hud_helmet

    if damage_protection=="yes":
        session["damage_protection"]=100
    else:
        session["damage_protection"]=0

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
        "normal_helmet": normal_helmet,
        "bluetooth_helmet": bluetooth_helmet,
        "hud_helmet": hud_helmet,
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

    return render_template("rent_duration.html", back_url="/rider-info")

@app.route("/save-rent", methods=["POST"])
def save_rent():

    start_day = request.form.get("start_day")
    end_day = request.form.get("end_day")

    start_day=datetime.strptime(start_day, "%Y-%m-%d")
    end_day=datetime.strptime(end_day, "%Y-%m-%d")

    today=datetime.today().date()

    if end_day<start_day:
        flash("End date cannot be before Start date","error")
        return redirect(url_for("rent_duration"))
    
    if end_day.date() < today:
        flash("End date cannot be before today", "error")
        return redirect(url_for("rent_duration"))
    
    # ❌ start date past me nahi hona chahiye
    if start_day.date() < today:
        flash("Start date cannot be in past", "error")
        return redirect(url_for("rent_duration"))
    
    rent_data = {
        "user_name": session["user_name"],
        "start_day": start_day,
        "end_day": end_day,
    }

    rents.insert_one(rent_data)

    flash("Helmet rental verification completed", "success")

    return redirect(url_for("payment"))

#---------Payment--------------------
@app.route("/payment")
def payment():

    if "user_name" not in session:
        return redirect(url_for("login"))

    normal=session.get("normal_helmet",0)
    bluetooth=session.get("bluetooth_helmet",0)
    hud=session.get("hud_helmet",0)
    damage=session.get("damage_protection",0)

    normal_price=50
    bluetooth_price=200
    hud_price=300

    # fetch rent data
    rent = rents.find_one({"user_name": session["user_name"]}, sort=[("_id", -1)])

    start_day = rent["start_day"]
    end_day = rent["end_day"]

    # calculate days
    days = (end_day - start_day).days + 1

    total_price = (
        (normal*normal_price) + \
                (bluetooth*bluetooth_price)+ \
                (hud*hud_price)
    ) * days+damage

    return render_template("payment.html",
                           normal=normal,
                           bluetooth=bluetooth,
                           hud=hud,
                           damage=damage,
                           days=days,
                           total_price=total_price,
                           back_url="/rent-duration")

# -------- Booking Complete Page --------
@app.route("/booking-success")
def booking_success():

    if "user_name" not in session:
        return redirect(url_for("login"))

    return render_template("booking_success.html", back_url="/payment")

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

#-----------Forgot Password-------------
@app.route("/forgot-password")
def forgot_password():
    return render_template("forgot_password.html")

#----------------Reset Password----------------
@app.route("/reset-password", methods=["POST"])
def reset_password():

    email = request.form.get("email").lower()
    answer = request.form.get("security_answer").lower()
    new_password = request.form.get("new_password")

    user = users.find_one({"email": email})

    if not user:
        flash("Email not found", "error")
        return redirect(url_for("forgot_password"))

    if user["security_answer"] != answer:
        flash("Wrong security answer", "error")
        return redirect(url_for("forgot_password"))

    # update password
    users.update_one(
        {"email": email},
        {"$set": {"password": new_password}}
    )

    flash("Password reset successful", "success")
    return redirect(url_for("login"))

# Logout
@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully.", "info")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)