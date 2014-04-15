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

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    user = User(request.form["name"], request.form["email"],
                request.form["password"])
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

    registered_user = User.query.filter_by(email=email, password=password).first()
    if registered_user is None:
        flash("Email or Password is invalid", "danger")
        return redirect(url_for("login"))
    login_user(registered_user, remember=remember_me)
    flash("Logged in successfully", "success")
    return redirect(request.args.get("next") or url_for("index"))

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
    salt = db.Column("salt", db.String(32))
    registered_on = db.Column("registered_on", db.DateTime)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

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
