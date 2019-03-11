from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class AdminForm(FlaskForm):
    course_code = StringField('Course Code', validators=[DataRequired()])
    student_name = StringField('Student Name', validators=[DataRequired()])
    student_email = StringField('Student Email', validators=[DataRequired()])
    group = StringField('Group', validators=[DataRequired()])
    start_time = StringField('Start Time', validators=[DataRequired()])
    end_time = StringField('End Time', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])

    submit = SubmitField('Sign In')

