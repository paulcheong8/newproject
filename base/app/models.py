from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKeyConstraint
import datetime

student_course_table = db.Table('student_course', 
db.Column('student_id', db.Integer, db.ForeignKey('student.id'), primary_key=True), 
db.Column('course_id', db.Integer, db.ForeignKey('course.id'), primary_key=True) )

class Admin(UserMixin, db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<Admin {}>'.format(self.email)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class StudentLogin(UserMixin, db.Model):
    __tablename__ = 'studentlogin'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<Student Login   {}>'.format(self.email)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Student(db.Model):
    __tablename__ = 'student'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    # One to many relationship with Mac 
    addresses = db.relationship('Mac', back_populates='student', cascade='all', lazy=True, uselist=True)
    # Many to Many relationship with Course
    courses = db.relationship('Course', secondary=student_course_table, lazy='joined', back_populates='students')
    
    def __init__(self, name, email, addresses=None, courses=None): 
        self.name = name 
        self.email = email 
        addresses = [] if addresses is None else addresses 
        self.addresses = addresses 
        courses = [] if courses is None else courses 
        self.courses = courses

    def __repr__(self):
        return '<Student {}>'.format(self.name)

    def serialize(self): 
        return { 
            'id': self.id, 
            'name': self.name,
            'email': self.email,
            'addresses': [a.serialize() for a in self.addresses],
            'courses':[c.serialize() for c in self.courses]
        }

class Mac(db.Model):
    __tablename__ = 'mac'

    id = db.Column(db.Integer, primary_key=True)
    mac_address = db.Column(db.String(80), unique=True, nullable=False)
    # Many to one relationship with Student
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False) 
    student = db.relationship('Student', back_populates='addresses')

    def __init__(self, mac_address, student_id): #readings=None): 
        self.mac_address = mac_address
        self.student_id = student_id

    def __repr__(self):
        return '<Mac {}>'.format(self.mac_address)

    def serialize(self): 
        return { 
            'id': self.id, 
            'mac_address': self.mac_address,
            'student_id': self.student_id
        }

class Course(db.Model): 
    __tablename__ = 'course' 
    
    id = db.Column(db.Integer, primary_key=True) 
    course_code = db.Column(db.String(120), unique=True, nullable=False)
    start_time = db.Column(db.String(120), unique=False, nullable=False) 
    end_time = db.Column(db.String(120), unique=False, nullable=False)  
    start_date = db.Column(db.String(120), unique=False, nullable=False)  
    end_date = db.Column(db.String(120), unique=False, nullable=False)  
    # Many to Many relationship with Student
    students = db.relationship('Student', secondary=student_course_table, lazy='joined', back_populates='courses')
    # Many to one relationship with Location
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False) 
    location = db.relationship('Location', back_populates='course')

    def __init__(self, course_code, start_time, end_time, start_date, end_date, location_id, students=None): 
        self.course_code = course_code 
        self.start_time = start_time
        self.end_time = end_time
        self.start_date = start_date
        self.end_date = end_date
        self.location_id = location_id
        students = [] if students is None else students 
        self.students = students 

    def __repr__(self):
        return '<Course {}>'.format(self.course_code)

    def serialize(self): 
        return { 
            'id': self.id, 
            'course_code': self.course_code,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'location_id': self.location_id,
            'students': [s.serialize() for s in self.students]
        }

class Location(db.Model):
    __tablename__ = 'location'

    id = db.Column(db.Integer, primary_key=True) 
    venue = db.Column(db.String(120), unique=True, nullable=False)
    # One to many relationship with Course
    course = db.relationship('Course', back_populates='location', cascade='all', lazy=True, uselist=True)
    # One to one relationship with Receiver
    receiver = db.relationship('Receiver', back_populates='location', cascade='all', lazy=True, uselist=True)

    def __init__(self, venue, course=None, receiver=None): 
        self.venue = venue 
        course = [] if course is None else course 
        self.course = course 
        receiver = [] if receiver is None else receiver 
        self.receiver = receiver

    def __repr__(self):
        return '<Location {}>'.format(self.venue)

    def serialize(self): 
        return { 
            'id': self.id, 
            'venue': self.venue,
            'course': [c.serialize() for c in self.course],
            'receiver':[r.serialize() for r in self.receiver]
        }

class Receiver(db.Model):
    __tablename__ = 'receiver'

    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(120), unique=True, nullable=False)
    # One to one relationship with Location
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False) 
    location = db.relationship('Location', back_populates='receiver')
    # One to many relationship with Readings
    # readings = db.relationship('Readings', back_populates='receiver', cascade='all', lazy=True, uselist=True)

    def __init__(self, name, location_id): #readings=None): 
        self.name = name 
        self.location_id = location_id
        # readings = [] if readings is None else readings 
        # self.readings = readings 

    def __repr__(self):
        return '<Receiver {}>'.format(self.name)

    def serialize(self): 
        return { 
            'id': self.id, 
            'name': self.name,
            'location_id': self.location_id
            # 'readings':[r.serialize() for r in self.receiver]
        }

class AttendanceTemp(db.Model):
    __tablename__ = 'attendance_temp'

    id = db.Column(db.Integer, primary_key=True) 
    count = db.Column(db.Integer, unique=False, nullable=False)
    student_id = db.Column(db.String(120), unique=False, nullable=False)
    course_id = db.Column(db.String(120), unique=False, nullable=False)

    def __init__(self, count, student_id, course_id):
        self.count = count
        self.student_id = student_id
        self.course_id = course_id

    def __repr__(self):
        return '<Attendance {}>'.format(self.id)

    def serialize(self): 
        return { 
            'id': self.id, 
            'status': self.count,
            'student_id': self.student_id,
            'course_id': self.course_id
        }

class Attendance(db.Model):
    __tablename__ = 'attendance'

    id = db.Column(db.Integer, primary_key=True) 
    status = db.Column(db.String(120), unique=False, nullable=False)
    student_id = db.Column(db.String(120), unique=False, nullable=False)
    course_id = db.Column(db.String(120), unique=False, nullable=False)
    week = db.Column(db.String(120), unique=False, nullable=False)

    def __init__(self, status, student_id, course_id, week):
        self.status = status
        self.student_id = student_id
        self.course_id = course_id
        self.week = week

    def __repr__(self):
        return '<Attendance {}>'.format(self.id)

    def serialize(self): 
        return { 
            'id': self.id, 
            'status': self.status,
            'student_id': self.student_id,
            'course_id': self.course_id,
            'week' : self.week
        }

@login.user_loader
def load_user(id):
    return Admin.query.get(int(id))