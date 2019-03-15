from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKeyConstraint

# student_course_table = db.Table('student_course', 
# db.Column('student_id', db.Integer, db.ForeignKey('student.id'), primary_key=True), 
# db.Column('course_id', db.Integer, db.ForeignKey('course.id'), primary_key=True) )

# class Admin(UserMixin, db.Model):
#     __tablename__ = 'admin'
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(120), index=True, unique=True)
#     password_hash = db.Column(db.String(128))

#     def __repr__(self):
#         return '<Admin {}>'.format(self.email)

#     def set_password(self, password):
#         self.password_hash = generate_password_hash(password)

#     def check_password(self, password):
#         return check_password_hash(self.password_hash, password)

#     # def serialize(self): 
#     #     return { 
#     #         'id': self.id, 
#     #         'email': self.email, 
#     #     }

# class Student(db.Model):
#     __tablename__ = 'student'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(80), unique=False, nullable=False)
#     email = db.Column(db.String(80), unique=True, nullable=False)
#     # many to many relationship with Course
#     courses = db.relationship('Course', secondary=student_course_table, lazy=True, back_populates='students')
#     # one to many relationship with Mac
#     mac_addresses = db.relationship('Mac', back_populates='student', cascade='all', lazy=True, uselist=True)


#     def __init__(self, name, email, courses=None, mac_addresses=None):
#         self.name = name
#         self.email = email
#         courses = [] if courses is None else courses
#         self.courses = courses
#         mac_addresses = [] if mac_addresses is None else mac_addresses
#         self.mac_addresses = mac_addresses

#     def __repr__(self):
#         return '<Student {}>'.format(self.name)

#     def serialize(self): 
#         return { 
#             'id': self.id, 
#             'name': self.name,
#             'email': self.email,
#             'courses':[c.serialize() for c in self.courses],
#             'mac_addresses': [m.serialize() for m in self.mac_addresses]
#         }

# class Mac(db.Model):
#     __tablename__ = 'mac'
#     id = db.Column(db.Integer, primary_key=True)
#     mac_address = db.Column(db.String(80), unique=True, nullable=False)
#     # foreign key with student
#     student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
#     # one to many relationship with student 
#     student = db.relationship('Student', back_populates='mac_addresses')
#     # for the foreign key with Readings
#     mac_addresses = db.relationship('Readings', back_populates='mac', cascade='all', lazy=True, uselist=True)


#     def __init__(self, mac_address, student_id, mac_addresses=None):
#         self.mac_address = mac_address
#         self.student_id = student_id
#         mac_addresses = [] if mac_addresses is None else mac_addresses
#         self.mac_addresses = mac_addresses


#     def __repr__(self):
#         return '<Mac {}>'.format(self.mac_address)

#     def serialize(self): 
#         return { 
#             'id': self.id, 
#             'mac_address': self.mac_address,
#             'student_id': self.student_id,
#             'mac_addresses': [m.serialize() for m in self.mac_addresses]
#         }

# class Course(db.Model):
#     __tablename__ = 'course'
#     id = db.Column(db.Integer, primary_key=True)
#     course_code = db.Column(db.String(120), index=True, unique=True)
#     start_time = db.Column(db.Integer, index=True, unique=False)
#     end_time = db.Column(db.Integer, index=True, unique=False)
#     # many to many relationship with Student 
#     students = db.relationship('Student', secondary=student_course_table, lazy=True, back_populates='courses')
#     # foreign key with Location
#     location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
#     locations = db.relationship('Location', back_populates='locations_course')

#     def __init__(self, course_code, start_time, end_time, location_id, students=None):
#         self.course_code = course_code
#         self.start_time = start_time
#         self.end_time = end_time
#         self.location_id = location_id
#         students = [] if students is None else students 
#         self.students = students

#     def __repr__(self):
#         return '<Class {}>'.format(self.course_code)
    
#     def serialize(self): 
#         return { 
#             'id': self.id,
#             'course_code': self.course_code,
#             'start_time': self.start_time,
#             'end_time': self.end_time,
#             'location_id': self.location_id,
#             'students':[s.serialize() for s in self.students] 
#         }

# class Location(db.Model):
#     __tablename__ = 'location'
#     id = db.Column(db.Integer, primary_key=True)
#     location = db.Column(db.String(120), unique=True, nullable=False)
#     # for the foreign key with Receiver
#     locations = db.relationship('Receiver', back_populates='location', cascade='all', lazy=True, uselist=True)
#     # for the foreign key with Course
#     locations_course = db.relationship('Course', back_populates='locations', cascade='all', lazy=True, uselist=True)

#     def __init__(self, location, locations, locations_course):
#         self.location = location
#         locations = [] if locations is None else location
#         self.locations = locations
#         locations_course = [] if locations_course is None else locations_course
#         self.locations_course = locations_course

#     def __repr__(self):
#         return '<Location {}>'.format(self.location)

#     def serialize(self): 
#         return { 
#             'id': self.id,
#             'location': self.location,
#             'locations': self.locations,
#             'locations_course': self.locations_course
#         } 

# class Readings(db.Model):
#     __tablename__ = 'readings'
#     id = db.Column(db.Integer, primary_key=True)
#     time_stamp = db.Column(db.String(120), index=True, unique=False)
#     # foreign key with Receiver
#     receiver_id = db.Column(db.Integer, db.ForeignKey('receiver.id'), nullable=False)
#     # receiver = relationship("Receiver", back_populates='receivers', foreign_keys=[receiver_id])
#     # # one to many relationship with Receiver
#     receiver = db.relationship('Receiver', back_populates='receivers')
#     # foreign key with Mac 
#     mac_id = db.Column(db.Integer, db.ForeignKey('mac.id'), nullable=False)
#     # mac = relationship("Mac", back_populates='mac_addresses', foreign_keys=[mac_id])
#     mac = db.relationship('Mac', back_populates='mac_addresses')


#     # __table_args__ = (
#     #     ForeignKeyConstraint(
#     #         ["receiver_id"],
#     #         ["mac_id"]
#     #     ),)

#     def __init__(self, time_stamp, receiver_id, mac_id):
#         self.time_stamp = time_stamp
#         self.receiver_id = receiver_id
#         self.mac_id = mac_id

#     def __repr__(self):
#         return '<Reader {}>'.format(self.id)

#     def serialize(self): 
#         return { 
#             'id': self.id,
#             'time_stamp': self.time_stamp,
#             'receiver_id': self.receiver_id,
#             'mac_id': self.mac_id
#         }   

# class Receiver(db.Model):
#     __tablename__ = 'receiver'
#     id = db.Column(db.Integer, primary_key=True)
#     # foreign key with Readings
#     readings_id = db.Column(db.Integer, db.ForeignKey('readings.id'), nullable=False)
#     # # one to many relationship with Readings
#     receivers = db.relationship('Readings', back_populates='receiver', cascade='all', lazy=True, uselist=True)
#     # foreign key with Location
#     location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
#     location = db.relationship('Location', back_populates='locations')

#     def __init__(self, location_id, readings_id):
#         self.location_id = location_id
#         self.readings_id = readings_id

#     def __repr__(self):
#         return '<Receiver {}>'.format(self.id)

#     def serialize(self): 
#         return { 
#             'id': self.id,
#             'location_id': self.location_id,
#             'readings_id': self.readings_id
#         }   

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

    # def serialize(self): 
    #     return { 
    #         'id': self.id, 
    #         'email': self.email, 
    #     }

class Student(db.Model):
    __tablename__ = 'student'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    # One to many relationship with Mac 
    addresses = db.relationship('Mac', back_populates='student', cascade='all', lazy=True, uselist=True)
    # Many to Many relationship with Course
    courses = db.relationship('Course', secondary=student_course_table, lazy=True, back_populates='students')
    
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
    __tablename__ = 'course' 
    
    id = db.Column(db.Integer, primary_key=True) 
    course_code = db.Column(db.String(120), unique=True, nullable=False)
    # day = db.Column(db.String(120), unique=True, nullable=False) 
    start_time = db.Column(db.String(120), unique=True, nullable=False) 
    end_time = db.Column(db.String(120), unique=True, nullable=False)  
    # Many to Many relationship with Student
    students = db.relationship('Student', secondary=student_course_table, lazy=True, back_populates='courses')
    # Many to one relationship with Location
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False) 
    location = db.relationship('Location', back_populates='course')

    def __init__(self, course_code, start_time, end_time, location_id, students=None): 
        self.course_code = course_code 
        self.start_time = start_time
        self.end_time = end_time
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
    readings = db.relationship('Readings', back_populates='receiver', cascade='all', lazy=True, uselist=True)

    def __init__(self, name, location_id, readings=None): 
        self.name = name 
        self.location_id = location_id
        readings = [] if readings is None else readings 
        self.readings = readings 

    def __repr__(self):
        return '<Receiver {}>'.format(self.name)

    def serialize(self): 
        return { 
            'id': self.id, 
            'name': self.name,
            'location_id': self.location_id,
            'readings':[r.serialize() for r in self.receiver]
        }

class Readings(db.Model):
    __tablename__ = 'readings'

    id = db.Column(db.Integer, primary_key=True) 
    #use datetime
    #time_stamp = db.Column(db.String(120), unique=True, nullable=False)
    # day = db.Column(db.String(120), unique=False, nullable=False)
    # time = db.Column(db.String(120), unique=False, nullable=False)
    mac_address = db.Column(db.String(120), unique=False, nullable=False)
    # Many to one relationship with Receiver
    receiver_id = db.Column(db.Integer, db.ForeignKey('receiver.id'), nullable=False) 
    receiver = db.relationship('Receiver', back_populates='readings')

    def __init__(self, time_stamp, mac_address, receiver_id): 
        self.time_stamp = time_stamp
        self.mac_address = mac_address 
        self.receiver_id = receiver_id

    def __repr__(self):
        return '<Readings {}>'.format(self.time_stamp)

    def serialize(self): 
        return { 
            'id': self.id, 
            'time_stamp': self.time_stamp,
            'mac_address': self.mac_address,
            'receiver_id': self.receiver_id
        }

@login.user_loader
def load_user(id):
    return Admin.query.get(int(id))

#this is change 1945