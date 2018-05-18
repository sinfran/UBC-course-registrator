from ssc import get_sessions
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired

class LoginForm (FlaskForm):
    username = StringField ('CWL Login', validators = [DataRequired ()])
    password = PasswordField ('Password', validators = [DataRequired ()])
    submit = SubmitField ('Submit')

class CourseSelectionForm (FlaskForm):
    ssc_data = get_sessions ()
    sessions = SelectField (label='Session', choices=[ (s,s) for s in ssc_data])
    subject_code = StringField ('Course Subject Code', validators = [DataRequired ()])
    course_num = StringField ('Course Number', validators = [DataRequired ()])
    section = StringField ('Section', validators = [DataRequired ()])
    submit = SubmitField ('Submit')

class MobileNotificationForm (FlaskForm):
    mobile_number = StringField ('Mobile Number:', validators = [DataRequired ()])
    submit = SubmitField ('Submit')

