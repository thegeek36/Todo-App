from flask import Blueprint, redirect, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Todo
from . import db


views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        if len(title) == 0:
            flash("Please Enter Title",category='error')
        todo = Todo(title=title,desc =desc,user_id=current_user.id)
        db.session.add(todo)
        db.session.commit()
    return render_template('index.html',user=current_user)

@views.route('/delete/<int:id>')
def delete(id):
    todo = Todo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

@views.route('/update/<int:id>',methods=['POST','GET'])
def update(id):
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(id=id).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        print(todo.title)
        return redirect("/")
    todo = Todo.query.filter_by(id=id).first()
    print(todo.title,"  ",todo.desc)
    return render_template("update.html",todo=todo,user=current_user)

@views.route('/about')
def about():
    return render_template('about.html',user=current_user)
