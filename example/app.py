import uuid
import bcrypt
import hashlib
import sendgrid
import datetime
from flask import Flask, session, request, flash, url_for, redirect, \
render_template, abort, g
from flask.ext.login import login_user, logout_user, current_user, \
login_required, LoginManager
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile("config.py")
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/protected")
@login_required
def protected():
    return render_template("protected.html")

@app.route("/unprotected")
def unprotected():
    return render_template("unprotected.html")

@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    user = User(request.form["name"], request.form["email"],
                request.form["password"])
    user.registered_on = datetime.datetime.now()
    db.session.add(user)
    db.session.commit()
    flash("User successfully registered", "success")
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    email = request.form["email"]
    password = request.form["password"]

    remember_me = False

    if "remember_me" in request.form:
        remember_me = True

    registered_user = User.query.filter_by(email=email).first()
    if registered_user is None:
        flash("Email is invalid", "danger")
        return redirect(url_for("login"))
    elif bcrypt.hashpw(password, registered_user.password) != registered_user.password:
        flash("Password is invalid", "danger")
        return redirect(url_for("login"))

    login_user(registered_user, remember=remember_me)
    flash("Logged in successfully", "success")
    return redirect(request.args.get("next") or url_for("index"))

@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "GET":
        return render_template("forgot-password.html")

    email = request.form["email"]

    user = User.query.filter_by(email=email).first()
    if user is None:
        flash("No user with this email exists", "danger")
        return redirect(url_for("forgot_password"))
    else:
        user.password_reset_hash = hashlib.sha1(uuid.uuid4().hex).hexdigest()
        user.password_reset_exp = datetime.datetime.now() + datetime.timedelta(days=1)
        db.session.merge(user)
        db.session.commit()
        sg = sendgrid.SendGridClient(app.config["SENDGRID_USER"],
                                     app.config["SENDGRID_PASS"])
        message = sendgrid.Mail(to=email, subject="Password Reset Link",
                                html="This password reset link will expire in 24 hours.",
                                text="This password reset link will expire in 24 hours.",
                                from_email=app.config["SEND_EMAIL_FROM"])
        status, msg = sg.send(message)
        flash("Password reset link has been sent", "success")
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.before_request
def before_request():
    g.user = current_user

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(db.Model):
    __tablename__ = "tbl_user"
    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(128))
    email = db.Column("email", db.String(128), unique=True, index=True)
    password = db.Column("password", db.String(60))
    password_reset_hash = db.Column("password_reset_hash", db.String(40))
    password_reset_exp = db.Column("password_reset_exp", db.DateTime)
    registered_on = db.Column("registered_on", db.DateTime)

    def __init__(self, name, email, plain_password):
        self.name = name
        self.email = email
        self.password = bcrypt.hashpw(plain_password, bcrypt.gensalt(app.config["BCRYPT_ITERATIONS"]))

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return True

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return "<User {0}>".format(self.email)

if __name__ == "__main__":
    app.run(port=5001)
