from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user
from robobrowser import RoboBrowser
from app.forms import LoginForm, CourseSelectionForm, MobileNotificationForm
from app.models import User
from app import app
import ssc
import re

br = None
course = None
request = None
session = None

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
    global course
    global request
    global session
    form = CourseSelectionForm ()
    if form.validate_on_submit ():
        year = re.search ('[0-9]{4}', form.sessions.data).group (0)
        term = re.search ('[S|W]', form.sessions.data).group (0)
        session_href = '/cs/main?sessyr=' + year + '&sesscd=' + term
        active_session = br.find_all ("li", {"class":"active"})[2].find ('a')
        active_session ['href'] = session_href
        br.open (ssc.base_url + active_session ['href'])
        br.open (ssc.browse_url)
        session = ssc.base_url + active_session ['href']
        subject_codes = br.find_all ("td")
        for s in subject_codes:
            subject_code_data = s.findAll (text = True)
            if (len (subject_code_data) == 3):
                if (subject_code_data [1] == form.subject_code.data):
                    br.open (ssc.base_url + s.find ('a') ['href']) # subject exists
                    courses = br.find_all ("td")
                    course_request = form.subject_code.data + " " + form.course_num.data
                    for course in courses:
                        if (course.findAll (text = True) [0] == course_request):
                            br.open (ssc.base_url + course.find ('a') ['href']) # course exists
                            sections = br.find_all ("td")
                            for section in sections:
                                if (len (section.findAll (text = True)) > 1):
                                    course_request = form.subject_code.data + " " + form.course_num.data + " " + form.section.data
                                    if (section.findAll (text = True) [1].strip () == course_request):
                                        request = ssc.base_url + section.find ('a') ['href']
                                        br.open (request)
                                        
                                        course = course_request
                                        return redirect (url_for ('results'))
    
        
        return redirect (url_for ('index'))
    return render_template ('index.html', title='UBC Course Registrator', form=form)

@app.route ('/results', methods=[ 'GET', 'POST' ])
def results ():
    global br
    global course
    course_data = br.find_all ("td")
    for index, d in enumerate (course_data):
        if (d.findAll (text = True) [0] == 'Total Seats Remaining:'):
            num_seats = course_data [index + 1].findAll (text = True) [0]
    return render_template ('results.html', title='UBC Course Registrator', course = course, seats=str (num_seats))

@app.route ('/twilio', methods=[ 'GET', 'POST' ])
def twilio ():
    form = MobileNotificationForm ()
    # mobile = '+1' + form.mobile_number.data
    
    return render_template ('twilio.html', title='UBC Course Registrator', form=form)






