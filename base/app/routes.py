from app import app
from flask import render_template, request, redirect, url_for, flash
from app import db
from app.models import Student, Course, Readings, Receiver, Admin
from app.forms import LoginForm, AdminForm
from flask_login import current_user, login_user, logout_user

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Paul'}
    return render_template('index.html', user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():
        admin = Admin.query.filter_by(email=form.username.data).first()

        if admin is None or not admin.check_password(form.password.data):
            flash('Invalid email or password')
            return redirect(url_for('login'))

        login_user(admin, remember=form.remember_me.data)
        return redirect(url_for('admin'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    form = AdminForm()
    if form.validate_on_submit():

        course = Course(course_code=form.course_code.data, 
        start_time=form.start_time.data,
        end_time=form.end_time.data)

        db.session.add(course)
        db.session.commit()

        flash ('Course information has been updated!')
        return redirect(url_for('admin'))
    return render_template('admin.html', title='Course', form=form)
    
    
@app.route('/student')
def student():
    return render_template('student.html', title='Home')

@app.route('/post_student', methods=['POST'])
def post_student():
    student = Student(request.form['name'], request.form['email'])
    
    db.session.add(student)
    db.session.commit()
    return redirect(url_for('student')) 

# @app.route('/post_admin', methods=['POST'])
# def post_admin():
#     course = Class(request.form['course_code'], request.form['student_name'], request.form['student_email'], request.form['group'], request.form['start_time'], request.form['end_time'])
#     db.session.add(course)
#     db.session.commit()
#     return redirect(url_for('admin')) 


