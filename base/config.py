import os
basedir = os.path.abspath(os.path.dirname(__file__))
class Config(object):

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    # SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:Chicken101@localhost/SmartAttendance'
    SQLALCHEMY_DATABASE_URI = 'postgres://hysfhbmhjxdqeu:b3663b1293e45b7e55ac63d419eead755a786af9e7212def3bb7ff851ccf95cb@ec2-184-72-238-22.compute-1.amazonaws.com:5432/dbjcr7q3pq6tq3'

    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')

#     POSTGRES = {
#     'user': 'postgres',
#     'pw': 'Chicken101',
#     'db': 'SmartAttendance',
#     'host': 'localhost',
#     'port': '5432'
#     }

#     DEBUG = True


#     SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:\
# %(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
#     SQLALCHEMY_TRACK_MODIFICATIONS = False