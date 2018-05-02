from twilio.rest import Client
from robobrowser import RoboBrowser
from credentials import account_sid, auth_token, my_cell, my_twilio
import config
import sys
import re

SSC_LOGIN_PORTAL = "https://cas.id.ubc.ca/ubc-cas/login?TARGET=https%3A%2F%2Fcourses.students.ubc.ca%2Fcs%2Fsecure%2Flogin%3FIMGSUBMIT.x%3D50%26IMGSUBMIT.y%3D18%26IMGSUBMIT%3DIMGSUBMIT"
SSC_BASE_URL = "https://courses.students.ubc.ca"
SSC_BROWSE_URL = SSC_BASE_URL + "/cs/main?pname=subjarea&tname=subjareas&req=0"

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
def exit ():
    config.cls ()
    sys.exit ("Login failed.")

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
        exit ()
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

    selection = int (input ("\nSelect a session (e.g. \"1\"): ")) - 1
    session_href = sessions [selection].get ('href')
    active_session ['href'] = sessions [selection].get ('href')
    br.open (SSC_BASE_URL + active_session ['href'])
    br.open (SSC_BROWSE_URL)

def select_course ():
    global br
    request = None
    # Prompt user to enter subject code and course number
    requested_subject_code = input ("Enter Subject Code (e.g. \"CPSC\"): ")
    requested_course_num = input ("Enter Course Number: ")
    requested_course = requested_subject_code + " " + requested_course_num

    subject_codes = br.find_all ("td")
    for s in subject_codes:
        subject_code_data = s.findAll (text = True)
        if (len (subject_code_data) == 3):
            if (subject_code_data [1] == requested_subject_code):
                request = s.find ('a') ['href']
                break
    
    br.open (SSC_BASE_URL + request)
  
    courses = br.find_all ("td")
    for course in courses:
        if (course.findAll (text = True) [0] == requested_course):
            request = course.find ('a') ['href']


    br.open (SSC_BASE_URL + request)
    sections = br.find_all ("td")
    requested_section = input ("Enter Course Section: ")

    requested_course = requested_subject_code + " " + requested_course_num + " " + requested_section

    for section in sections:
        if (len (section.findAll (text = True)) > 1):
            if (section.findAll (text = True) [1].strip () == requested_course):
                request = section.find ('a') ['href']
                break

    br.open (SSC_BASE_URL + request)


def check_seats ():
    global br
    course_data = br.find_all ("td")
    for index, d in enumerate (course_data):
        if (d.findAll (text = True) [0] == 'Total Seats Remaining:'):
            num_seats_available = int (course_data [index + 1].findAll (text = True) [0])
            if (num_seats_available > 0):
                client.messages.create (to = my_cell, from_ = my_twilio, body = "There are " + str (num_seats_available) + " seats available.")
                exit ()
            else:
                print ("No seats available.")
            break


def main ():
    init_r_browser (SSC_LOGIN_PORTAL)
    login_and_validate ()
    select_session ()
    select_course ()
    check_seats ()
    


main ()















