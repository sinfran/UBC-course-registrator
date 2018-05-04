from twilio.rest import Client
from robobrowser import RoboBrowser
from credentials import account_sid, auth_token, my_cell, my_twilio
import config
import sys
import re

SSC_LOGIN_PORTAL = "https://cas.id.ubc.ca/ubc-cas/login?TARGET=https%3A%2F%2Fcourses.students.ubc.ca%2Fcs%2Fsecure%2Flogin%3FIMGSUBMIT.x%3D50%26IMGSUBMIT.y%3D18%26IMGSUBMIT%3DIMGSUBMIT"
SSC_BASE_URL = "https://courses.students.ubc.ca"
SSC_BROWSE_URL = SSC_BASE_URL + "/cs/main?pname=subjarea&tname=subjareas&req=0"


#https://courses.students.ubc.ca/cs/main?pname=subjarea&tname=subjareas&req=5&dept=PSYC&course=305A&section=921


client = None
br = None

# Initialize RoboBrowser and Twilio
def init_r_browser (url):
    global br
    global client
    client = Client (account_sid, auth_token)
    br = RoboBrowser (parser = 'html.parser')
    br.open (url)

# Terminate program
def exit (msg):
    config.cls ()
    if (msg == None): sys.exit ("Invalid request.")
    else: sys.exit (msg)

def handle_form ():
    global br
    form = br.get_form ()
    form ['username'] = config.DATACOUP_USERNAME
    form ['password'] = config.DATACOUP_PASSWORD
    config.cls ()
    print ("Logging in...")
    br.submit_form (form)
    return br.find_all ('td')

def login_and_validate ():
    table_data = handle_form ()
    if len (table_data) == 0: # Handle unsuccessful login
        exit ("Login failed.")
    name = re.search ('%s(.*)%s' % ('<strong>', '</strong>'), str (table_data [0])).group (1)
    config.cls ()
    print ("Login successful.\nHello " + name + "!\n")

def select_session ():
    global br
    sessions = br.select ('a[href^="/cs/main?sessyr="]')
    active_session = br.find_all ("li", {"class":"active"})[2].find ('a')
    print ("Sessions:")

    for index, session in enumerate (sessions):
        print (''.join (session.findAll (text = True)) + " [" + str (index + 1) + "]")

    user_request = int (input ("\nSelect a session (e.g. \"1\"): ")) - 1

    try:
        session_href = sessions [user_request].get ('href')
        active_session ['href'] = session_href
        br.open (SSC_BASE_URL + active_session ['href'])
        br.open (SSC_BROWSE_URL)
    except Exception:
        exit (None)

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
        exit ("Requested course does not exist.")
    return href

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

def find_section (req):
    global br
    href = None
    sections = br.find_all ("td")
    for section in sections:
        if (len (section.findAll (text = True)) > 1):
            if (section.findAll (text = True) [1].strip () == req):
                request = section.find ('a') ['href']
                break
    if (href == None):
        exit ("Requested course does not exist.")
    return href




def select_course ():
    global br
    # Prompt user to enter subject code and course number
    requested_subject_code = input ("Enter Subject Code (e.g. \"CPSC\"): ")
    requested_course_num = input ("Enter Course Number: ")
    requested_course = requested_subject_code + " " + requested_course_num

    request = find_subject (requested_subject_code)
    br.open (SSC_BASE_URL + request)
  
    request = find_course (requested_course)
    br.open (SSC_BASE_URL + request)

    requested_section = input ("Enter Course Section: ")
    requested_course = requested_subject_code + " " + requested_course_num + " " + requested_section

    request = find_section (requested_course)


    while (1):
        check_seats (request)


def check_seats (request):
    global br
    br.open (SSC_BASE_URL + request)
    course_data = br.find_all ("td")
    for index, d in enumerate (course_data):
        if (d.findAll (text = True) [0] == 'Total Seats Remaining:'):
            num_seats_available = int (course_data [index + 1].findAll (text = True) [0])
            if (num_seats_available > 0):
                client.messages.create (to = my_cell, from_ = my_twilio, body = "There are " + str (num_seats_available) + " seats available.")
                exit ("")
                # else:
                #    print ("No seats available.")
#break


def main ():
    init_r_browser (SSC_LOGIN_PORTAL)
    login_and_validate ()
    select_session ()
    select_course ()
    while (1):
        check_seats ()
    


main ()















