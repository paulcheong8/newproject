from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField, RadioField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename 

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class StudentForm(FlaskForm):
    #name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    mac_addresses = StringField('Mac Address', validators=[DataRequired()])
    submit = SubmitField('Add')

class ReceiverForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    submit = SubmitField('Add')
    
class AdminForm(FlaskForm):
    course_code = StringField('Course Code', validators=[DataRequired()])
    student_details = FileField(validators=[FileRequired()])
    start_time = StringField('Start Time', validators=[DataRequired()])
    end_time = StringField('End Time', validators=[DataRequired()])
    start_date = StringField('Start Date', validators=[DataRequired()])
    end_date = StringField('End Date', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    submit = SubmitField('Add')

class AttendanceForm(FlaskForm):
    course_code = StringField('Course', validators=[DataRequired()])
    attendance_type = RadioField('Type', choices=[('current','Current'),('historical','Historical')])
    submit = SubmitField('Search')