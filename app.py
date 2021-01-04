
# A very simple Flask Hello World app for you to get started with...

from flask import Flask , render_template, redirect, url_for, request, session

app = Flask(__name__)
app.secret_key = "hello"

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
        return redirect(url_for("user"))
    else:
        if "user" in session:
            return redirect(url_for("user"))
        return render_template("login.html")

@app.route("/user")
def user():
    if "user" in session:
        user = session["user"]
        return f'<h4><a class="nav-link active" aria-current="page" href="http://sms3750.pythonanywhere.com">Thank you for visiting {user}</a></h4> '
    else:
        return redirect(url_for("login"))
@app.route("/logout",methods=["POST","GET"])
def logout():
    session.pop("user",None)
    return redirect(url_for("login"))
