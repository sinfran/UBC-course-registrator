from twilio.rest import Client
from robobrowser import RoboBrowser
from twilio_credentials import account_sid, auth_token, my_cell, my_twilio
import config
import ssc
import sys
import re


course_url = None
session_url = None
SSC_COURSE_URL = None
SSC_SESSION_URL = None

client = None
br = None
course_request = None

# Initialize RoboBrowser and Twilio
def init (url):
    global br
    global client
    client = Client (account_sid, auth_token)
    br = RoboBrowser (parser = 'html.parser')
    br.open (url)
    config.DATACOUP_MOBILE = '+1' + str (config.DATACOUP_MOBILE)

# Terminate program
def exit (msg):
    config.cls ()
    if (msg == None): sys.exit ("Invalid request.")
    else: sys.exit (msg)

# Handle login form
def handle_form ():
    global br
    form = br.get_form ()
    form ['username'] = config.DATACOUP_USERNAME
    form ['password'] = config.DATACOUP_PASSWORD    
    config.cls ()
    print ("Logging in...")
    br.submit_form (form)
    return br.find_all ('td')

# Validate user login
def login_and_validate ():
    table_data = handle_form ()
    if len (table_data) == 0:
        exit ("Login failed.")
    name = re.search ('%s(.*)%s' % ('<strong>', '</strong>'), str (table_data [0])).group (1)
    config.cls ()
    print ("Login successful.\nHello " + name + "!\n")

def select_session ():
    global br
    global session_url
    sessions = br.select ('a[href^="/cs/main?sessyr="]')
    active_session = br.find_all ("li", {"class":"active"})[2].find ('a')
    print ("Sessions:")
    for index, session in enumerate (sessions):
        print (''.join (session.findAll (text = True)) + " [" + str (index + 1) + "]")
    user_req = int (input ("\nSelect a session (e.g. \"1\"): ")) - 1
    try:
        session_href = sessions [user_req].get ('href')
        active_session ['href'] = session_href
        session_url = ssc.base_url + active_session ['href']
        br.open (session_url)
        br.open (ssc.browse_url)
    except Exception:
        exit (None)

# Find requested subject on SSC
def find_subject (req):
    global br
    href = None
    subject_codes = br.find_all ("td")
    for s in subject_codes:
        subject_code_data = s.findAll (text = True)
        if (len (subject_code_data) == 3):
            if (subject_code_data [1] == req):
                href = s.find ('a') ['href']
                break
    if (href == None):
        exit ("Requested subject does not exist.")
    return href

# Find requested course on SSC
def find_course (req):
    global br
    href = None
    courses = br.find_all ("td")
    for course in courses:
        if (course.findAll (text = True) [0] == req):
            href = course.find ('a') ['href']
    if (href == None):
        exit ("Requested course does not exist.")
    return href

# Find requested course section on SSC
def find_section (req):
    global br
    href = None
    sections = br.find_all ("td")
    for section in sections:
        if (len (section.findAll (text = True)) > 1):
            if (section.findAll (text = True) [1].strip () == req):
                href = section.find ('a') ['href']
                break
    if (href == None):
        exit ("Requested section does not exist.")
    return href

def select_course ():
    global br
    global course_request
    subj_req = input ("Enter Subject Code (e.g. \"CPSC\"): ")
    num_req = input ("Enter Course Number: ")
    course_request = subj_req + " " + num_req
    request = find_subject (subj_req)
    br.open (ssc.base_url + request)
    request = find_course (course_request)
    br.open (ssc.base_url + request)
    section_req = input ("Enter Course Section: ")
    course_request = subj_req + " " + num_req + " " + section_req
    request = find_section (course_request)
    check_seats (request)

def register ():
    global br
    data = br.find_all ("a")
    for d in data:
        d_text = d.findAll (text = True)
        if (len (d_text) > 0):
            if (d_text [0] == 'Register Section'):
                href = d ['href']
                br.open (ssc.base_url + href)

def check_seats (request):
    global br
    global course_url
    course_url = ssc.base_url + request
    br.open (course_url)
    course_data = br.find_all ("td")
    for index, d in enumerate (course_data):
        if (d.findAll (text = True) [0] == 'Total Seats Remaining:'):
            num_seats_available = int (course_data [index + 1].findAll (text = True) [0])
            if (num_seats_available > 0):
                register ()
                twilio_notify (str (num_seats_available))
                exit ("")
            else:
                twilio_notify (0)

# Send user a mobile notification when space is available
def twilio_notify (seats):
    if (seats == 0):
        msg = "There are currently no seats available for " + course_request + ". A mobile notification will be sent as soon as space becomes available!"
        print (msg)
    else:
        msg = "There are currently " + seats + " seat(s) available for " + course_request + ". Attempted auto-registration. Check SSC to see if it was successful."
    client.messages.create (to = config.DATACOUP_MOBILE, from_ = my_twilio, body = msg)

def keep_checking ():
    global br
    try:
        br.open (ssc.browse_url)
        br.open (session_url)
        br.open (course_url)
        course_data = br.find_all ("td")
        for index, d in enumerate (course_data):
            if (d.findAll (text = True) [0] == 'Total Seats Remaining:'):
                num_seats_available = int (course_data [index + 1].findAll (text = True) [0])
                if (num_seats_available > 0):
                    register ()
                    twilio_notify (str (num_seats_available))
                    exit ("")
    except Exception:
        exit (None)


def main ():
    init (ssc.login_portal)
    login_and_validate ()
    select_session ()
    select_course ()
    while (True): keep_checking ()
    

main ()















