from flask import Blueprint ,render_template, request, redirect, url_for, session
from flask_login import current_user, login_required
from .models import Task
import json

views = Blueprint("views", __name__)

@views.route("/")
def home():
    return render_template("index.html", user=current_user)

@views.route("/tasks", methods=["GET", "POST"])
@login_required
def tasks():
    if request.method == "POST":
        task_name = request.form.get("task-select")
        # print(task.id)
        # task = json.dumps({"task": task})
        return redirect(url_for("views.question", user=current_user, task_name=task_name))

    return render_template("tasks.html", user=current_user)

@views.route("/tasks/questions", methods=["GET", "POST"])
@login_required
def question():
    name = request.args["task_name"]
    task = Task.query.filter_by(user_id=current_user.id, name=name).first()
    # print(task.id)

    if request.method == "POST":
        print(request.form.get("question-select"))
    
    return render_template("questions.html", user=current_user, task=task)