from flask import Blueprint ,render_template, request, flash, redirect, url_for
from flask_login import login_user, current_user, logout_user, login_required
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db


auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()
        if not user:
            flash("Lietotājs neeksistē!", category="error")
        elif not check_password_hash(user.password, password):
            flash("Nepareiza parole!", category="error")
        else:
            login_user(user, remember=True)
            flash("Pieslēgšanās veiksmīga!", category="success")
            return redirect(url_for("views.home"))
        

    return render_template("login.html", user=current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    # print("POST")
    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        user = User.query.filter_by(username=username).first()

        if user:
            flash("Lietotājvārds jau pastāv!", category="error")
        elif len(first_name) < 2:
            flash("Vārdam ir jābūt vismaz 2 zīmes garam!", category="error")
        elif len(last_name) < 2:
            flash("Uzvārdam ir jābūt vismaz 2 zīmes garam!", category="error")
        elif len(username) < 4:
            flash("Lietotājvārdam ir jābūt vismaz 4 zīmes garam!", category="error")
        elif password1 != password2:
            flash("Paroles nav vienādas!", category="error")
        elif len(password1) < 8:
            flash("Parolei ir jābūt vismaz 8 zīmes garai!", category="error")
        else:
            new_user = User(first_name=first_name, last_name=last_name, username=username, password=generate_password_hash(password1, "sha256"))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("Lietotājs ir izveidots!", category="success")
            return redirect(url_for("views.home"))
    return render_template("sign_up.html", user=current_user)
