from app import app
from flask import render_template, request, redirect, url_for, flash, jsonify
from app import db
from app.models import Student, Course, Admin, Mac, Location, Receiver, Readings
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

#daryl de 
@app.route('/addcourse', methods=["POST"])
def add_course():
    course_code = request.json["course_code"]
    emails = request.json["emails"]
    names = request.json["names"]
    start_time = request.json["start_time"]
    end_time = request.json["end_time"]
    location = request.json["location"]
    try:
        new_course = Course(course_code=course_code, start_time=start_time, end_time=end_time)
        db.session.add(new_course)
        db.session.commit()
        for i in range(len(emails)):
            new_email = emails[i]
            new_name = names[i]
            new_student = Student(email=new_email,name=new_name)
            db.session.add(new_student)
            db.session.commit()
        new_location = Location(location=location)
        db.session.add(new_location)
        db.session.commit()
        return jsonify("{} was created".format(new_course))
    except Exception as e:
        return (str(e))

@app.route('/updateMAC', methods=["POST","PUT"])
def add_mac():
    try:
        for mac in request.json["mac_addresses"]:
            email = request.json["email"]
            mac_address= mac
            student = Student.query.get(email)
            SID = student.id
            new_mac = Mac(mac_address=mac_address, student_id = SID, mac_addresses = None)
            db.session.add(new_mac)
            db.session.commit()
        return jsonify("{} was created".format(new_mac))
    except Exception as e:
        return (str(e))


#daryl de

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


