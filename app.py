
# A very simple Flask Hello World app for you to get started with...

from flask import Flask , render_template, redirect, url_for, request, session, flash
#from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
import platform

# dictionary
info = {}

# platform details
platform_details = platform.platform()

# adding it to dictionary
info["platform details"] = platform_details

# system name
system_name = platform.system()

# adding it to dictionary
info["system name"] = system_name

# processor name
processor_name = platform.processor()

# adding it to dictionary
info["processor name"] = processor_name

# architectural detail
architecture_details = platform.architecture()

# adding it to dictionary
info["architectural detail"] = architecture_details

# printing the details

app = Flask(__name__)
app.secret_key = "hello"

db= SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

class users(db.Model):
    _id = db.Column("id",db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(80))
    def __init__(self,name,email):
        self.name = name
        self.email = email

@app.route("/")
def template():
    return render_template("template.html")
    #f"Thank you {name} for visiting this silmo.ml"

@app.route("/home/")
def home():
    return render_template("home.html")

@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/login",methods=["POST","GET"])
def login():
    if request.method == "POST":
        user = request.form["nm"]
        session["user"] = user
        found_user = users.query.filter_by(name=user).first()
        if found_user:
            session["email"]=found_user.email

        else:

            usr = users(user,"")
            db.session.add(usr)
            db.session.commit()

        flash(f"You are logged as {user}!","info")
        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash(f"You are already logged as {user}!","info")
            return redirect(url_for("user"))
        return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html", info=info)

@app.route("/user",methods=["POST","GET"])
def user():
    email = None
    if "user" in session:
        user = session["user"]
        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            found_user = users.query.filter_by(name=user).first()
            found_user.email=email
            db.session.commit()
            flash("Email was saved")
        else:
            if "email" in session:
                email = session["email"]
        return render_template("user.html", email = email,name=user)
    else:
        flash(f"Need to log-in","info")
        return redirect(url_for("login"))

@app.route("/logout",methods=["POST","GET"])
def logout():
    flash(f"You have been logged out!","info")
    session.pop("user",None)
    session.pop("email",None)

    return redirect(url_for("login"))


db.create_all()
if __name__ == "__main__":
    app.run()
