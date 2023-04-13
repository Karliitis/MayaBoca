from flask import Blueprint ,render_template, request, redirect, url_for, session, flash, jsonify, abort
from flask_login import current_user, login_required
from .models import Task, Question, Answer
from . import db
import json

views = Blueprint("views", __name__)

@views.route("/")
def home():
    return render_template("index.html", user=current_user)

@views.route("/tasks", methods=["GET", "POST"])
@login_required
def tasks():
    if request.method == "POST":
        task_id = request.form.get("task-select")
        return redirect(url_for("views.questions", task=task_id))

    return render_template("tasks.html", user=current_user)

@views.route("/tasks/questions", methods=["GET", "POST"])
@login_required
def questions():
    task_id = request.args["task"]
    task = Task.query.filter_by(user_id=current_user.id, id=task_id).first()

    if not task:
        abort(404)

    if request.method == "POST":
        question_id = request.form.get("question")
        add_question = request.form.get("add-question")
        if add_question:
            question = Question(question="Jauns jautājums", task_id=task_id)
            db.session.add(question)
            db.session.commit()
            question_id = question.id
            answer = Answer(answer="", question_id=question_id)
            db.session.add(answer)
            db.session.commit()
            
            
        # question =  Question.query.filter_by(task_id=task.id, question=question_name).first()
        return redirect(url_for("views.question", task=task_id, question=question_id))
    
    return render_template("questions.html", user=current_user, task=task)


@views.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", user=current_user)

@views.route("/tasks/questions/question", methods=["GET", "POST"])
@login_required
def question():
    task_id = int(request.args["task"])
    question_id = int(request.args["question"])
    task = Task.query.filter_by(user_id=current_user.id, id=task_id).first()
    question = Question.query.filter_by(task_id=task.id, id=question_id).first()

    if not task or not question or task.user_id != current_user.id:
        abort(404)

    if request.method == "POST":
        form = dict(request.form)
        question_name = form.pop("question")
        for _id, answer_name in form.items():
            answer = Answer.query.get(_id)
            if answer:
                if answer.question_id != question_id:
                    continue
                answer.answer = answer_name
            else:
                print(_id)
                # answer = Answer(answer=answer_name, question_id=question_id)
                # db.session.add(answer)
        db.session.commit()

        if len(question_name) < 1:
            flash("Nosaukumam ir jābūt vismaz 1 zīmi garam!", category="error")
        else:
            question.question = question_name
            db.session.commit()
            return redirect(url_for("views.questions", task=task_id))
    
    return render_template("question.html", user=current_user, question=question)



@views.route("/new-task", methods=["GET", "POST"])
@login_required
def new_task():
    if request.method == "POST":
        name = request.form.get("name")
        task = Task.query.filter_by(user_id=current_user.id, name=name).first()
        if task:
            flash("Šāda nosaukuma uzdevums jau eksistē!", category="error")
        elif len(name) < 1:
            flash("Nosaukumam ir jābūt vismaz 1 zīmi garam!", category="error")
        else:
            task = Task(name=name, user_id=current_user.id)
            db.session.add(task)
            db.session.commit()
            flash("Uzdevums izveidots", category="success")
            return redirect(url_for("views.tasks"))

    return render_template("new_task.html", user=current_user)

@views.route("/delete-task", methods=["POST"])
def delete_task():
    task = json.loads(request.data)
    task_id = task["taskId"]
    task = Task.query.get(task_id)
    if task and task.user_id == current_user.id:
        db.session.delete(task)
        db.session.commit()
    return jsonify({})

@views.route("/delete-question", methods=["POST"])
def delete_question():
    question = json.loads(request.data)
    question_id = question["questionId"]
    question = Question.query.get(question_id)
    task = Task.query.get(question.task_id)
    if question and task and task.user_id == current_user.id:
        db.session.delete(question)
        db.session.commit()

    return jsonify({})

@views.route("/delete-answer", methods=["POST"])
def delete_answer():
    answer = json.loads(request.data)
    answer_id = answer["answerId"]
    answer = Answer.query.get(answer_id)
    if answer:
        db.session.delete(answer)
        db.session.commit()
        print("deleted")
    return jsonify({})

@views.route("/add-answer", methods=["GET", "POST"])
def add_answer():
    question = json.loads(request.data)
    # question = Question.query.get(question)
    answer = Answer(answer="", question_id=question["questionId"])
    db.session.add(answer)
    db.session.commit()
    print(answer.id)
    return {"answerId": answer.id}
    