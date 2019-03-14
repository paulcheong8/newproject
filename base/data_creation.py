# from app import db 
# from app.models import Admin

# a = Admin(email='testing@gmail.com')
# a.set_password('123456')
# db.session.add(a)
# db.session.commit()

from app import db 
from app.models import Admin, Course, Mac, Location, Student, Receiver, Readings
from flask import request, json

# l = Location(venue='CR-3-3')
# db.session.add(l)
# db.session.commit()

c = Course(course_code='SMT440', start_time='0800', end_time='1130')
db.session.add(c)
db.session.commit()

s = Student(email='test@hello.com', name='tester')
db.session.add(s)
db.session.commit()