from app import db 
from app.models import Admin

a = Admin(email='testing2@gmail.com')
a.set_password('123456')
db.session.add(a)
db.session.commit()