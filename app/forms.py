from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

# DataRequired validator checks that the field is not empty
class LoginForm (FlaskForm):
    username = StringField ('CWL Login', validators = [DataRequired ()])
    password = PasswordField ('Password', validators = [DataRequired ()])
    submit = SubmitField ('Submit')
