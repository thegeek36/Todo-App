from datetime import datetime
from flask import Blueprint, redirect, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Todo
from . import db,app
from flask_mail import Mail, Message

# from config import MAIL_SERVER, MAIL_PORT, MAIL_USE_SSL, MAIL_USERNAME, MAIL_PASSWORD
views = Blueprint('views', __name__)
mail = Mail(app)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        if len(title) == 0:
            flash("Please Enter Title",category='error')
        else:
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
        #todo.date_created = datetime.now().strftime('%B %d %Y - %I:%M %p')
        db.session.add(todo)
        db.session.commit()
        print(todo.title)
        email = current_user.email
        name = current_user.first_name
        msg = Message('Your Task is Updated',sender='pptodo01@gmail.com', recipients=[email])#request.form['email']
        email_content = render_template('updateemail.html', title=title, des =desc,name = name)
        msg.html = email_content
        mail.send(msg)
        return redirect("/")
    todo = Todo.query.filter_by(id=id).first()
    print(todo.title,"  ",todo.desc)
    return render_template("update.html",todo=todo,user=current_user)

@views.route('/about')
def about():
    return render_template('about.html',user=current_user)
