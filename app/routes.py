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
                                        br.open (ssc.base_url + section.find ('a') ['href'])
                                        print ("reached here.")
                                        course_data = br.find_all ("td")
                                        for index, d in enumerate (course_data):
                                            if (d.findAll (text = True) [0] == 'Total Seats Remaining:'):
                                                print (int (course_data [index + 1].findAll (text = True) [0]))
        
        return redirect (url_for ('index'))
    return render_template ('index.html', title='UBC Course Registrator', form=form)

@app.route ('/results')
def results ():
    global br
    
    
    return None





