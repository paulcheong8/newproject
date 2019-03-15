from app import app, db
from app.models import Admin
from datetime import datetime

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Admin': Admin}

# while True:
#     current_time = datetime.datetime.now()

#     coursetime = "" #eg 12:00
#     coursetime = datetime.strptime(coursetime, "%H:%M")

#     coursestartdate = "" #eg 25/08
#     lessondate = datetime.strptime(coursetime, "%H:%M")

#     coursedates = {} #dictionary that has lesson_number:lesson_date
#     for i in range(1,13):
#         current_lesson = "lesson{}".format(i)
#         if i == 8:
#             lessondate += datetime.timedelta(days=7)
#         coursedates[current_lesson] = lessondate
#         lessondate += datetime.timedelta(days=7)


#     student_mac_dict = {} #get a dictionary that can store SID : mac address
#     macs = Mac.query.all()
#     for m in macs: 
#         mac_address = m.mac_address 
#         student_id = m.student_id
#         student_mac[student_id] = mac_address

#     mac_list = []

#     reciever_output = []

#     courselocation = "" #eg SIS SR2-4 get from receiver 