from app import app
from flask import render_template, request, redirect, url_for, flash, jsonify
from app import db
from app.models import Student, Course, Admin, Mac, Location, Receiver, Attendance
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

@app.route('/addcourse', methods=["POST"])
def add_course():
    course_code = request.json["course_code"]
    emails = request.json["emails"]
    names = request.json["names"]
    start_time = request.json["start_time"]
    end_time = request.json["end_time"]
    start_date = request.json['start_date']
    end_date = request.json['end_date']
    location = request.json["location"]
    try:
        # query if the location already exists then:
        # Location.query.filter_by(venue=location).first() == True
        if db.session.query(Location).filter(Location.venue==location).first() == True:
            new_location = db.session.query(Location).filter(Location.venue==location).first() 

        else: 
            new_location = Location(venue=location)
            db.session.add(new_location)
            db.session.commit()
        
        student_array = []
        for i in range(len(emails)):
            new_email = emails[i]
            new_name = names[i]
            new_student = Student(email=new_email,name=new_name)
            db.session.add(new_student)
            student_array.append(new_student)

        new_course = Course(course_code=course_code, start_time=start_time, end_time=end_time, 
        start_date=start_date, end_date=end_date ,location_id=new_location.id, students=student_array)
        db.session.add(new_course)
        db.session.commit()

        return jsonify("{} was created".format(new_course))
    except Exception as e:
        return (str(e))

@app.route('/updateMAC', methods=["POST","PUT"])
def add_mac():
    try:
        mac_addresses = request.json['mac_addresses']
        emails = request.json['email']
        for i in range(len(mac_addresses)):
            mac_address = mac_addresses[i]
            email = emails[i]
            student = db.session.query(Student).filter(Student.email==email).first()
            SID = student.id
            new_mac = Mac(mac_address=mac_address, student_id=SID)
            db.session.add(new_mac)
            db.session.commit()
        return jsonify("{} was created".format(new_mac))
    except Exception as e:
        return (str(e))

@app.route('/addReceiver', methods=['POST'])
def addReceiver():
    try:
        name = request.json['name']
        # how to input with the location_id parameter? 
        location_temp = request.json["location"]
        location = db.session.query(Location).filter(Location.venue==location_temp).first()
        LID = location.id
        new_receiver = Receiver(name=name, location_id=LID)
        db.session.add(new_receiver)
        db.session.commit()
        return jsonify("{} was created".format(new_receiver))
    except Exception as e:
        return (str(e))

@app.route('/addReadings', methods =['POST'])
def addreadings():
    try:
        student_mac_dict = {} #get a dictionary that can store SID : mac address
        instances_required = 12 #depending on lesson duration
        cid = 1 #cid of course
        macs = Mac.query.all()
        for m in macs: 
            mac_address = m.mac_address 
            student_id = m.student_id
            student_mac_dict[student_id] = mac_address
            
        student_id = []
        student_name = []
        student_email = []
        students = Student.query.all()
        for s in students:
            sid = s.id
            student_id.append(sid)
            sname = s.name
            student_name.append(sname)
            semail = s.email
            student_email.append(semail)
        
        reciever_output = request.json['macs'] #retrieve data from job
        attendance = {}
        for sid,mac in student_mac_dict:
            if mac in reciever_output:
                if sid not in attendance:
                    attendance[sid] = 1
                else:
                    attendance[sid] += 1

        attendance_recorded = []
        for sid,count in attendance:
            if count >= instances_required:
                if sid not in attendance_recorded:
                    new_attendance = Attendance(status="Present", student_id=sid, course_id=cid)
                    db.session.add(new_attendance)
                    db.session.commit()
                    attendance_recorded.append(sid)
        live_output = {
            "course_group" : "",
            "time" : "",
            "student_names" : student_name,
            "email": student_email,
            "attendance": attendance
        }
        #send -> location, student_id, student_name, student_email, attendance
        return render_template("display.php",student_dict = live_output)
    except Exception as e:
        return (str(e))

# @app.route('/getAttendance', methods=['GET'])
# def getAttendance():

# @app.route('/createReadings', methods=['POST'])
# def createReadings():
#     try:
#         # time_stamp = request.json['time_stamp']
#         mac_address = request.json['mac_address']
#         # check if mac_address exists in Mac.query.all()
#         new_reading = Readings(mac_address=mac_address, time_stamp=time_stamp)
#         #check if receiver_id exists in the Receiver table 
#         # how to get get the receiver_id parameter? 
#         db.session.add(new_reading)
#         db.session.commit()
#         return jsonify("{} was created".format(new_reading))

#     except Exception as e:
#         return (str(e))

#check if time is in Course[time] and day in Course[day] and Student in Course to get attendance

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


