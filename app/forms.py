
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired
from robobrowser import RoboBrowser


def get_sessions ():
    br = RoboBrowser (parser = 'html.parser')
    br.open ('https://courses.students.ubc.ca/cs/main?newSession=true')
    sessions = br.select ('a[href^="/cs/main?sessyr="]')
    choices = []
    for session in sessions:
        choices.append (''.join (session.findAll (text = True)))
    print (choices)
    return choices

# DataRequired validator checks that the field is not empty
class LoginForm (FlaskForm):
    username = StringField ('CWL Login', validators = [DataRequired ()])
    password = PasswordField ('Password', validators = [DataRequired ()])
    submit = SubmitField ('Submit')

class CourseSelectionForm (FlaskForm):
    data = get_sessions ()
    sessions = SelectField (label='Session', choices=[ (s,s) for s in data])
    

    #session = StringField ('Session', validators = [DataRequired ()])
    subject_code = StringField ('Course Subject Code', validators = [DataRequired ()])
    course_num = StringField ('Course Number', validators = [DataRequired ()])
    section = StringField ('Section', validators = [DataRequired ()])
    submit = SubmitField ('Submit')


