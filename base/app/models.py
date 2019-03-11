from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

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
    email = db.Column(db.String(120), index=True, unique=True)
    mac_address = db.Column(db.String(120), index=True, unique=True)

    def __init__(self, email, mac_address):
        self.email = email
        self.mac_address = mac_address

    def __repr__(self):
        return '<Student {}>'.format(self.email)

    def serialize(self): 
        return { 
            'id': self.id, 
            'email': self.email, 
            'mac_address': self.mac_address 
        }


class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String(120), index=True, unique=True)
    student_name = db.Column(db.String(120), index=True, unique=False)
    student_email = db.Column(db.String(120), index=True, unique=True)
    group = db.Column(db.String(3), index=True, unique=True)
    start_time = db.Column(db.Integer, index=True, unique=False)
    end_time = db.Column(db.Integer, index=True, unique=False)
    location = db.Column(db.String(120), index=True, unique=False)

    def __init__(self, course_code, student_name, student_email, group, start_time, end_time, location):
        self.course_code = course_code
        self.student_name = student_name
        self.student_email = student_email
        self.group = group
        self.start_time = start_time
        self.end_time = end_time
        self.location = location

    def __repr__(self):
        return '<Class {}>'.format(self.course_code)
    
    def serialize(self): 
        return { 
            'id': self.id,
            'course_code': self.course_code,
            'student_name': self.student_name, 
            'student_email': self.student_email,
            'group': self.group,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'location': self.location
        }


class Reader(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    receiver_id = db.Column(db.String(120), index=True, unique=True)
    mac_address = db.Column(db.String(120), index=True, unique=False)
    time_stamp = db.Column(db.String(120), index=True, unique=False)

    def __init__(self, receiver_id, mac_address, time_stamp):
        self.receiver_id = receiver_id
        self.mac_address = mac_address
        self.time_stamp = time_stamp

    def __repr__(self):
        return '<Reader {}>'.format(self.receiver_id)

    def serialize(self): 
        return { 
            'id': self.id,
            'receiver_id': self.receiver_id,
            'mac_address': self.mac_address,
            'time_stamp': self.time_stamp 
        }   


class Receiver(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    receiver_id = db.Column(db.String(120), index=True, unique=True)
    location = db.Column(db.String(120), index=True, unique=False)

    def __init__(self, receiver_id, location):
        self.receiver_id = receiver_id
        self.location = location

    def __repr__(self):
        return '<Receiver {}>'.format(self.receiver_id)

    def serialize(self): 
        return { 
            'id': self.id,
            'receiver_id': self.receiver_id,
            'location': self.location
        }   

@login.user_loader
def load_user(id):
    return Admin.query.get(int(id))