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

@app.route ('/index', methods=[ 'GET', 'POST' ])
def index ():
    global br
    form = CourseSelectionForm ()
    if form.validate_on_submit ():
        year = re.search ('[0-9]{4}', form.sessions.data).group (0)
        term = re.search ('[S|W]', form.sessions.data).group (0)
        session_href = '/cs/main?sessyr=' + year + '&sesscd=' + term
        
        active_session = br.find_all ("li", {"class":"active"})[2].find ('a')
        active_session ['href'] = session_href
        br.open (ssc.base_url + active_session ['href'])
        br.open (ssc.browse_url)
    return render_template ('index.html', title='UBC Course Registrator', form=form)





