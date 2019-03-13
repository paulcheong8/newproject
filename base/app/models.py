from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

student_course_table = db.Table('student_course', 
db.Column('student_id', db.Integer, db.ForeignKey('student.id'), primary_key=True), 
db.Column('course_id', db.Integer, db.ForeignKey('course.id'), primary_key=True) )

class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<Admin {}>'.format(self.email)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # def serialize(self): 
    #     return { 
    #         'id': self.id, 
    #         'email': self.email, 
    #     }

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    # many to many relationship with Course
    courses = db.relationship('Course', secondary=student_course_table, lazy=True, back_populates='students')
    # one to many relationship with Mac
    mac_addresses = db.relationship('Mac', back_populates='student', cascade='all', lazy=True, uselist=True)


    def __init__(self, name, email, courses=None, mac_addresses=None):
        self.name = name
        self.email = email
        courses = [] if courses is None else courses
        self.courses = courses
        mac_addresses = [] if mac_addresses is None else mac_addresses
        self.mac_addresses = mac_addresses

    def __repr__(self):
        return '<Student {}>'.format(self.name)

    def serialize(self): 
        return { 
            'id': self.id, 
            'name': self.name,
            'email': self.email,
            'courses':[c.serialize() for c in self.courses],
            'mac_addresses': [m.serialize() for m in self.mac_addresses]
        }

class Mac(db.model):
    id = db.Column(db.Integer, primary_key=True)
    mac_address = db.Column(db.String(80), unique=True, nullable=False)
    # foreign key with student
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    # one to many relationship with student 
    student = db.relationship('Student', back_populates='mac_addresses')
    # for the foreign key with Readings
    mac_addresses = db.relationship('Readings', back_populates='Mac', cascade='all', lazy=True, uselist=True)


    def __init__(self, mac_address, student_id):
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
    id = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String(120), index=True, unique=True)
    start_time = db.Column(db.Integer, index=True, unique=False)
    end_time = db.Column(db.Integer, index=True, unique=False)
    # many to many relationship with Student 
    students = db.relationship('Student', secondary=student_course_table, lazy=True, back_populates='courses')

    def __init__(self, course_code, start_time, end_time, students=None):
        self.course_code = course_code
        self.start_time = start_time
        self.end_time = end_time
        students = [] if students is None else students 
        self.students = students

    def __repr__(self):
        return '<Class {}>'.format(self.course_code)
    
    def serialize(self): 
        return { 
            'id': self.id,
            'course_code': self.course_code,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'students':[s.serialize() for s in self.students] 
        }

class Readings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time_stamp = db.Column(db.String(120), index=True, unique=False)
    # foreign key with Receiver
    receiver_id = db.Column(db.Integer, db.ForeignKey('receiver.id'), nullable=False)
    # one to many relationship with Receiver
    receiver = db.relationship('Receiver', back_populates='receivers')
    # foreign key with Mac 
    mac_id = db.Column(db.Integer, db.ForeignKey('mac.id'), nullable=False)
    mac = db.relationship('Mac', back_populates='mac_addresses')


    def __init__(self, time_stamp, receiver_id):
        self.time_stamp = time_stamp
        self.receiver_id = receiver_id

    def __repr__(self):
        return '<Reader {}>'.format(self.id)

    def serialize(self): 
        return { 
            'id': self.id,
            'time_stamp': self.time_stamp,
            'receiver_id': self.receiver_id,
        }   

class Receiver(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # one to many relationship with Readings
    receivers = db.relationship('Readings', back_populates='receiver', cascade='all', lazy=True, uselist=True)
    # foreign key with Location
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    location = db.relationship('Location', back_populates='locations')

    def __init__(self, location_id):
        self.location_id = location_id

    def __repr__(self):
        return '<Receiver {}>'.format(self.id)

    def serialize(self): 
        return { 
            'id': self.id,
            'location_id': self.location_id
        }   

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(120), unique=True, nullable=False)
    # for the foreign key with Receiver
    locations = db.relationship('Receiver', back_populates='location', cascade='all', lazy=True, uselist=True)

    def __init__(self, location):
        self.location = location

    def __repr__(self):
        return '<Location {}>'.format(self.location)

    def serialize(self): 
        return { 
            'id': self.id,
            'location_id': self.location
        } 
#cannot pushhhhhh
@login.user_loader
def load_user(id):
    return Admin.query.get(int(id))