import os
basedir = os.path.abspath(os.path.dirname(__file__))
class Config(object):

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    # SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:Chicken101@localhost/SmartAttendance'
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    # LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    SQLALCHEMY_DATABASE_URI = 'postgres://lgibhcwcleouzl:4e13a89c0c0b64ec0f0e0ea916456888d697630cc8fdf40af9977ecb4cd0cec2@ec2-23-23-241-119.compute-1.amazonaws.com:5432/da6um0if08b6hq'
# export DATABASE_URL="postgresql://lgibhcwcleouzl:4e13a89c0c0b64ec0f0e0ea916456888d697630cc8fdf40af9977ecb4cd0cec2@ec2-23-23-241-119.compute-1.amazonaws.com:5432/da6um0if08b6hq"
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