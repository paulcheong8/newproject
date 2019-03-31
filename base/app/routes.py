from app import app
from flask import render_template, request, redirect, url_for, flash, jsonify, json
from app import db
from app.models import Student, Course, Admin, Mac, Location, Receiver, Attendance, StudentLogin, AttendanceTemp, student_course_table
from app.forms import LoginForm, AdminForm, StudentForm, ReceiverForm, AttendanceForm
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta

@app.route('/')
def index():
    return redirect(url_for('login'))

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

        if db.session.query(db.exists().where(Location.venue==location)).scalar():
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
        if db.session.query(db.exists().where(Location.venue==location)).scalar():
        # if db.session.query(Location).filter(Location.venue==location).first() == True:
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

@app.route('/deleteReceiver/<name>', methods=["DELETE"])
def deleteReceiver(name):
    receiver = Receiver.query.get(name)
    if receiver == None:
        flash ('Please enter a vaid receiver name')
    else:
        db.session.delete(name)
        db.session.commit()
        return jsonify('Raspi {} was deleted'.format(name))

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

@app.route('/deletecourse/<course_id>', methods = ["DELETE"])
def delete_course(course_id):
    course = Course.query.get(course_id)
    if course == None:
        flash ('Please enter a valid course ID')
    else:
        db.session.delete(course)
        db.session.commit()
        return jsonify('{} was deleted'.format(course_id))

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

@app.route('/attendance', methods=["GET", "POST"])
@login_required
def attendance():
    form = AttendanceForm()
    if form.validate_on_submit():
        course_code = form.course_code.data
        attendance_type = form.attendance_type.data
        # check if it is a valid course input from the user 
        if db.session.query(db.exists().where(Course.course_code == course_code)).scalar():
            course = db.session.query(Course).filter(Course.course_code==course_code).first() 
            course_code = course.course_code
            course_id = course.id
            if attendance_type == 'current': 
                return redirect(url_for('displayLiveAttendance', course_code=course_code, course_id=course_id))
            else: 
                return redirect(url_for('AttendanceOverview', course_code=course_code, course_id=course_id))

        else:
            flash ('Please enter a valid course code!')
            return render_template('attendance.html', title='Attendance', form=form)

    return render_template('attendance.html', title='Attendance', form=form)
     
@app.route('/addReadings', methods =['POST'])
def addreadings():
    try:
        student_mac_dict = {} #get a dictionary that can store SID : mac address
        instances_required = 12 #depending on lesson duration

        current_datetime = datetime.now()
        datetime_string = datetime.now().strftime("%Y-%m-%d %H:%M") # cannot use timedelta
        date = datetime_string.split(' ')[0] 
        macs = request.json['macs']
        receiver_name = request.json['name']

##### NEED TO UNIQUELY IDENTIFY THE COURSE BECAUSE ONE RECEIVER CAN SERVE MANY COURSES ######

        receiver = db.session.query(Receiver).filter(Receiver.name==receiver_name).first() 
        location_id = receiver.location_id
        # each location definitely belongs to exactly one course thats why dont need validation 
        course = db.session.query(Course).filter(Course.location_id==location_id).first()
        # check date and time to verify that the record is during class time and only to be updated in this period
        course_id = course.id
        print ("this is courseID: ",course_id)
        start_date = course.start_date
        end_date = course.end_date
        start_time = course.start_time
        end_time = course.end_time
        start_datetime = str(start_date) + ' ' + str(start_time)
        end_datetime = str(start_date) + ' ' + str(end_time)

        class_start_datetime = datetime.strptime(start_datetime, "%Y-%m-%d %H:%M")
        class_end_datetime = datetime.strptime(end_datetime, "%Y-%m-%d %H:%M")

        course_start_datetime = datetime.strptime(start_date, "%Y-%m-%d")

        # create an array of the course datetime objects 
        course_dates_array = []
        num_days = 0
        for week_num in range(14):
            if week_num == 0: 
                num_days = 7
                course_dates_array.append(str(start_date))
            else:
                course_start_datetime += timedelta(days=num_days)
                course_date = course_start_datetime.strftime("%Y-%m-%d")
                course_dates_array.append(course_date)

        for i in course_dates_array:
            if date == i:
                week = course_dates_array.index(i) + 1
                print ("current time: ", current_datetime)
                print ("end time: ", class_end_datetime)
                print ("start time: ", class_start_datetime)
                class_end_datetime += timedelta(days=course_dates_array.index(i)*7)
                class_start_datetime += timedelta(days=course_dates_array.index(i)*7)

                if current_datetime < class_end_datetime and current_datetime > class_start_datetime:
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
                                        
                    for sid,mac in student_mac_dict.items():
                        if mac in reciever_output:
                            if str(sid) not in attendance:
                                attendance[str(sid)] = 1
                            else:
                                attendance[str(sid)] += 1
                    
########## why doesnt the count increase more than 11? #############
                    for sid,count in attendance.items():
                        if count >= instances_required:
                            # if student record does not exist in Attendance, => create a record
                            if not db.session.query(db.exists().where(Attendance.student_id == str(sid))).scalar():
                                new_attendance = Attendance(status="Present", student_id=sid, course_id=course_id, week=week)
                                db.session.add(new_attendance)
                                db.session.commit()
                            else:
                                attendance_records = db.session.query(Attendance).filter(Attendance.student_id==sid).all()
                                course_records = []
                                week_records = []
                                for record in attendance_records:
                                    course_records.append(record.course_id)
                                    week_records.append(record.week)
                                # validation for subsequent week's attends for that one course 
                                if (week not in week_records) and (course_id in course_records):
                                    new_attendance = Attendance(status="Present", student_id=sid, course_id=course_id, week=week)
                                    db.session.add(new_attendance)
                                    db.session.commit()
                                # validation for a new course's attendance
                                if (week not in week_records) and (course_id not in course_records):
                                    new_attendance = Attendance(status="Present", student_id=sid, course_id=course_id, week=week)
                                    db.session.add(new_attendance)
                                    db.session.commit()

                        else:
                            if db.session.query(db.exists().where(AttendanceTemp.student_id == str(sid))).scalar():
                                row = db.session.query(AttendanceTemp).filter(AttendanceTemp.student_id==sid).first()
                                print (row.count)
                                row.count = count
                                db.session.commit()
                            else:
                                tempattendance = AttendanceTemp(count=count, student_id=sid, course_id=course_id)
                                db.session.add(tempattendance)
                                db.session.commit()
                
                    return "Updated Successfully!"

# line below is to delete all rows in the AttendanceTemp when the class ends 

                # elif current_datetime > class_start_datetime:
                #     absent = db.session.query(AttendanceTemp).filter(AttendanceTemp.count < instances_required).all()
                #     for a in absent:
                #         sid = a.student_id
                #         new_attendance = Attendance(status="Absent", student_id=sid, course_id=course_id, week=week)
                #         db.session.add(new_attendance)
                #         db.session.commit()
                #     attendance_temp = AttendanceTemp.query.all()
                #     for a in attendance_temp:
                #         db.session.delete(a)


    except Exception as e:
        return (str(e))

@app.route('/displayLiveAttendance/<course_code>/<course_id>/', methods =['GET', 'POST'])
@login_required
def displayLiveAttendance(course_code, course_id):

    student_id = []
    student_name = []
    student_email = []
    date = (datetime.now().strftime("%Y-%m-%d %H:%M"))

    all = db.session.query(student_course_table).all()

    for i in all:
        print (type(i[1]))
        if i[1] == int(course_id):
            student_id.append(i[0])
            student = db.session.query(Student).filter(Student.id==str(i[0])).first()
            sname = str(student.name)
            student_name.append(sname)
            semail = str(student.email)
            student_email.append(semail)

    attendance_count = []

    for id in student_id:
        if db.session.query(db.exists().where(AttendanceTemp.student_id == str(id))).scalar():
            attendance = db.session.query(AttendanceTemp).filter(AttendanceTemp.student_id==str(id)).first()
            attendance_count.append(attendance.count)
        else:
            attendance_count.append(0)
    
    return render_template(
        "displayLive.html",
        date=date,
        course_code=course_code,
        student_id=student_id,
        student_name=student_name,
        student_email=student_email,
        attendance_count=attendance_count)

@app.route('/AttendanceOverview/<course_code>/<course_id>/', methods =['GET', 'POST'])
@login_required
def AttendanceOverview(course_code,course_id):
    week = "week01" #depending on start date of course

    student_name = []
    student_id = []
    student_email = []
    attendance = Attendance.query.filter_by(course_id=course_id).all()
    status = []
    week = []

    for i in range(len(attendance)):
        
        student = Student.query.filter_by(id=attendance[i].student_id).first()
        student_id.append(student.id)
        student_name.append(student.name)
        student_email.append(student.email)
        
        status.append(attendance[i].status)
    
    return render_template(
        "displayOverview.html",
        course_code=course_code,
        student_name=student_name,
        student_email=student_email,
        status=status)

@app.route('/getStudentAttendance/<student_email>', methods=["GET"])
def getStudentAttendance(student_email):

    student = Student.query.filter_by(email=student_email).first()
    student_id = student.id

    student_attendance = Attendance.query.filter_by(student_id=student_id).first()
    return jsonify(student_attendance.serialize())

if __name__ == '__main__':
	app.run(debug=True)