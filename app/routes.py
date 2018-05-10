from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user
from robobrowser import RoboBrowser
from app.forms import LoginForm, CourseSelectionForm
from app.models import User
from app import app
import ssc
import re

br = None

@app.route ('/')
@app.route('/login', methods=[ 'GET', 'POST' ])
def login ():
    global br
    login = LoginForm ()
    if login.validate_on_submit ():
        br = RoboBrowser (parser = 'html.parser')
        br.open (ssc.login_portal)
        form = br.get_form ()
        form ['username'] = login.username.data
        form ['password'] = login.password.data
        br.submit_form (form)
        table_data = br.find_all ('td')
        if len (table_data) == 0:
            flash ('Invalid username or password')
            return redirect (url_for ('login'))
        else:
            name = re.search ('%s(.*)%s' % ('<strong>', '</strong>'), str (table_data [0])).group (1)
            user = User (id=name)
            login_user (user)
            return redirect (url_for ('index'))
    return render_template ('login.html', title='Sign In', form=login)

@app.route ('/index')
def index ():
    global br
    form = CourseSelectionForm ()
    return render_template ('index.html', title='UBC Course Registrator', form=form)





