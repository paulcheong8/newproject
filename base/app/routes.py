from app import app
from flask import render_template, request, redirect, url_for, flash, jsonify, json
from app import db
from app.models import Student, Course, Admin, Mac, Location, Receiver, Attendance, StudentLogin, AttendanceTemp
from app.forms import LoginForm, AdminForm, StudentForm, ReceiverForm, AttendanceForm
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.utils import secure_filename

@app.route('/')
# @app.route('/index')
# def index():
#     user = {'username': 'Paul'}
#     return render_template('index.html', user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(email=form.username.data).first()
        student = StudentLogin.query.filter_by(email=form.username.data).first()
        if (admin is None or not admin.check_password(form.password.data)) and (student is None or not student.check_password(form.password.data)):
            flash('Invalid email or password')
            return redirect(url_for('login'))
        elif admin is not None and admin.check_password(form.password.data) == True:
            login_user(admin, remember=form.remember_me.data)
            return redirect(url_for('admin'))
        elif student is not None and student.check_password(form.password.data) == True:
            login_user(student, remember=form.remember_me.data)
            return redirect(url_for('student'))

    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    return render_template('admin.html', title='Admin')

@app.route('/admin/updateinformation', methods=['GET', 'POST']) # tested and working 
@login_required
def updateInformation():
    form = AdminForm()
    if form.validate_on_submit():
        course_code = form.course_code.data
        course_code = form.course_code.data
        start_time = form.start_time.data
        end_time = form.end_time.data
        start_date = form.start_date.data
        end_date = form.end_date.data
        location = form.location.data

        student_array = []
        student_details = form.student_details.data
        # filename = secure_filename(student_details.filename)
        contents = student_details.read()

        contents_stripped = contents.rstrip("\r\n")
        contents_split = contents_stripped.split("\r\n")
        first_row = True
        for content in contents_split:
            if first_row == True:
                first_row = False
            else: 
                data = content.split(",")
                new_name = data[0]
                new_email = data[1]
                if not db.session.query(db.exists().where(Student.email == new_email)).scalar():
                    new_student = Student(email=new_email, name=new_name)
                    db.session.add(new_student)
                    student_array.append(new_student)

        if db.session.query(Location).filter(Location.venue==location).first() == True:
            new_location = db.session.query(Location).filter(Location.venue==location).first() 
        else: 
            new_location = Location(venue=location)
            db.session.add(new_location)
            db.session.commit()

        new_course = Course(course_code=course_code, 
        start_time=start_time, 
        end_time=end_time, 
        start_date=start_date, 
        end_date=end_date,
        location_id=new_location.id, 
        students=student_array)

        db.session.add(new_course)
        db.session.commit()

        flash ('Course information has been updated!')
        return redirect(url_for('updateInformation'))
    return render_template('updateinformation.html', title='Admin', form=form)

@app.route('/admin/addReceiver', methods=['GET', 'POST']) # tested and working 
@login_required
def admin_add_receiver():
    form = ReceiverForm()
    if form.validate_on_submit():
        name = form.name.data
        location = form.location.data

        if db.session.query(Location).filter(Location.venue==location).first() == True:
            location = db.session.query(Location).filter(Location.venue==location).first() 
            LID = location.id
        else: 
            new_location = Location(venue=location)
            db.session.add(new_location)
            db.session.commit()
            LID = new_location.id

        new_receiver = Receiver(name=name, location_id=LID)
        db.session.add(new_receiver)
        db.session.commit()

        flash ('Receiver has been updated!')
        return redirect(url_for('admin_add_receiver'))
    return render_template('adminaddreceiver.html', title='Admin', form=form)         

@app.route('/addReceiver', methods=['GET','POST']) # tested and working  
def addReceiver():
    try:
        name = request.json['name']
        print (name)
        location = request.json["location"]
        if db.session.query(Location).filter(Location.venue==location).first() == True:
            location = db.session.query(Location).filter(Location.venue==location).first() 
            LID = location.id
        else: 
            new_location = Location(venue=location)
            db.session.add(new_location)
            db.session.commit()
            LID = new_location.id

        new_receiver = Receiver(name=name, location_id=LID)
        db.session.add(new_receiver)
        db.session.commit()
        redirect(url_for('admin_add_receiver'))
        return jsonify("{} was created".format(new_receiver))
    except Exception as e:
        redirect(url_for('admin_add_receiver'))
        return (str(e))

@app.route('/student')
@login_required
def student():
    return render_template('student.html', title='Home')

@app.route('/student/addMac', methods=["GET", "POST"]) # tested and working 
@login_required
def student_add_mac():
    form = StudentForm()
    if form.validate_on_submit():
        mac_addresses = form.mac_addresses.data
        email = form.email.data
        name = form.name.data
        if ',' in mac_addresses:
            mac_addresses_array = mac_addresses.split(',')
        else:
            mac_addresses_array = [mac_addresses]

        for mac_address in mac_addresses_array: 
            if db.session.query(db.exists().where(Student.email == email)).scalar():
                student = db.session.query(Student).filter(Student.email==email).first()
                SID = student.id
                new_mac = Mac(mac_address=mac_address, student_id=SID)
                db.session.add(new_mac)
                db.session.commit()
            else: 
                new_student = Student(email=email, name=name)
                db.session.add(new_student)
                db.session.commit()
                SID = new_student.id
                new_mac = Mac(mac_address=mac_address, student_id=SID)
                db.session.add(new_mac)
                db.session.commit()

        flash ('Mac Address has been updated!')
        return redirect(url_for('student_add_mac'))
    return render_template('studentaddmac.html', title='Student', form=form)

@app.route('/attendance')
@login_required
def attendance():
    form = AttendanceForm()
    if form.validate_on_submit():
        course_code = form.course_code.data
        attendance_type = form.attendance_type.data
        
        if attendance_type == 'current': 
            return render_template('display.php', course_code=course_code)
        else: 
            return redirect(url_for('getAttendance', course_code=course_code))

    return render_template('attendance.html', title='Attendance', form=form)

@app.route('/addcourse', methods=["POST"]) # tested and working 
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

@app.route('/updateMAC', methods=["POST","PUT"]) # tested and working
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



@app.route('/addReadings', methods =['POST'])
def addreadings():
    try:
        student_mac_dict = {} #get a dictionary that can store SID : mac address
        instances_required = 12 #depending on lesson duration
        cid = 1 #cid of course
        week = "week01" #depending on start date of course
        course_group = "SMT201 G1"
        time = "1200H"

        macs = Mac.query.all()
        for m in macs: 
            mac_address = str(m.mac_address)
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
        attendancetemp = AttendanceTemp.query.all()
        attendance = {}
        for temp in attendancetemp: # if there is no entries will initialize to an empty dict
            sid = str(temp.student_id)
            count = temp.count
            attendance[sid] = count
        
        print(attendance)
        
        for sid,mac in student_mac_dict.items():
            if mac in reciever_output:
                if str(sid) not in attendance:
                    attendance[str(sid)] = 1
                else:
                    attendance[str(sid)] += 1

        print(attendance)
        
        for sid,count in attendance.items():
            if count >= instances_required:
                if not db.session.query(db.exists().where(Attendance.student_id == str(sid))).scalar():
                    new_attendance = Attendance(status="Present", student_id=sid, course_id=cid)
                    db.session.add(new_attendance)
                    db.session.commit()
            else:
                if db.session.query(db.exists().where(AttendanceTemp.student_id == str(sid))).scalar():
                    row = db.session.query(AttendanceTemp).filter(AttendanceTemp.student_id==sid).first()
                    print (row.count)
                    row.count = count
                    db.session.commit()
                else:
                    tempattendance = AttendanceTemp(count=count, student_id=sid, course_id=cid)
                    db.session.add(tempattendance)
                    db.session.commit()
       
        live_output = jsonify({
            "course_group" : course_group,
            "time" : time,
            "week" : week,
            "student_id" : student_id,
            "student_names" : student_name,
            "email": student_email,
            "attendance": attendance
        })
        
        #send -> location, student_id, student_name, student_email, attendance
        return render_template("display.php",student_dict = live_output)
    except Exception as e:
        return (str(e))

@app.route('/displayLiveAttendance', methods =['GET'])
def displayLiveAttendance():
    week = "week01" #depending on start date of course
    course_group = "SMT201 G1"
    time = "1200H"

    student_id = []
    student_name = []
    student_email = []
    students = Student.query.all()
    for s in students:
        sid = s.id
        student_id.append(sid)
        sname = str(s.name)
        student_name.append(sname)
        semail = str(s.email)
        student_email.append(semail)

    attendancetemp = AttendanceTemp.query.all()
    attendance = {}
    for temp in attendancetemp: # if there is no entries will initialize to an empty dict
        sid = str(temp.student_id)
        count = temp.count
        attendance[sid] = count

    live_output = {
        "course_group" : course_group,
        "time" : time,
        # "week" : week,
        "student_id" : student_id,
        "student_names" : student_name,
        "email": student_email,
        "attendance": attendance
        }
    
    print(live_output)

    # fp = open('/tmp/live_output', 'w+')
    # live_output = dict(json.dump(fp, live_output))

    live_output = json.dumps(live_output)
    print (type(live_output))

    return render_template(
        "display.php",
        course_group=course_group,
        time=time,
        student_id=student_id,
        student_name=student_name,
        student_email=student_email,
        attendance=attendance)

if __name__ == '__main__':
	app.run(debug=True)