import os

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, static_url_path='/static')
# Check for environment variable
#if not os.getenv("DATABASE_URL"):
#    raise RuntimeError("DATABASE_URL is not set")
#DATABASE_URL=$(heroku config:get DATABASE_URL -a book-review-db-1)
# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
#For Deployment
engine = create_engine(os.getenv("DATABASE_URL"))
#For Local
#engine = create_engine("postgres://rljdkhwyibrclr:83b8058cc1429ab991e99a6bdf0f137575a6a87654989daa21d4cce4891134fc@ec2-50-17-90-177.compute-1.amazonaws.com:5432/d2adq2pnnb6dg2")
db = scoped_session(sessionmaker(bind=engine))



@app.route("/",methods =["POST","GET"])
def index():
    if request.method=="POST":
        session.pop('id', None)
    if 'id' in session:
        return render_template("main.html")
    else:
        return render_template('login.html')

@app.route("/registration",methods =["POST","GET"])
def register():
    return render_template('registration.html')

@app.route("/registration/true?",methods =["POST"])
def check():
    username = request.form.get("username")
    password = request.form.get("password")
    new = db.execute("SELECT id FROM users WHERE username = :username",{"username":username}).fetchone()
    if new is None:
        password_h = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
        db.execute("INSERT INTO users (username, password_h) VALUES (:username, :password_h)",{"username": username, "password_h": password_h})
        db.commit()
        return render_template('registrationS.html')
    else:
        return render_template('registrationF.html')

@app.route("/main",methods =["POST","GET"])
def main():
    if request.method == "GET":
        if 'id' in session:
            return render_template("main.html")
        else:
            return render_template("loginF.html")
    else:
        username = request.form.get("username")
        password_inp = request.form.get("password")
        id = db.execute("SELECT id FROM users WHERE username = :username",{"username":username}).fetchone()
        db.commit()
        if id is None:
            return render_template("loginF.html")
        id = id[0]
        password = db.execute("SELECT password_h FROM users WHERE id = :id",{"id":id}).fetchone()
        db.commit()
        password=password[0]
        if check_password_hash(password,password_inp):
            session["id"] = id
            print(session["id"])
            return render_template("main.html")
        else:
            return render_template("loginF.html")

@app.route("/userinfo",methods = ["POST","GET"])
def user():
    id = session["id"]
    username = db.execute("SELECT username FROM users WHERE id = :id",{"id":id}).fetchone()
    username = username[0]
    db.commit()
    return render_template('userpage.html',username=username)

@app.route("/search",methods = ["POST","GET"])
def search():
    return "SEARCHPAGE"

@app.route("/API",methods = ["POST","GET"])
def api():
    return "API"
