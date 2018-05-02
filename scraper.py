from robobrowser import RoboBrowser
import request as req
import config
import sys
import re

base_url = "https://courses.students.ubc.ca"
browse_courses_url = "https://courses.students.ubc.ca/cs/main?pname=subjarea&tname=subjareas&req=0"

br = RoboBrowser (parser = 'html.parser')

br.open ("https://cas.id.ubc.ca/ubc-cas/login?TARGET=https%3A%2F%2Fcourses.students.ubc.ca%2Fcs%2Fsecure%2Flogin%3FIMGSUBMIT.x%3D50%26IMGSUBMIT.y%3D18%26IMGSUBMIT%3DIMGSUBMIT")

form = br.get_form ()
form ['username'] = config.DATACOUP_USERNAME
form ['password'] = config.DATACOUP_PASSWORD

config.cls ()
print ("Logging in...")

# Login
br.submit_form (form)
table = br.find_all ('td')
if len (table) == 0:
    config.cls ()
    sys.exit ("Login failed.")

# Validate login
start = '<strong>'
end = '</strong>'
name = re.search ('%s(.*)%s' % (start, end), str (table [0])).group (1)

config.cls ()
print ("Login successful.\nHello " + name + "!\n")

# Prompt user to select session
sessions = br.select ('a[href^="/cs/main?sessyr="]')
active_session = br.find_all ("li", {"class":"active"})[2].find ('a')

print ("Sessions:")
for index, session in enumerate (sessions):
    print (''.join (session.findAll (text = True)) + " [" + str (index + 1) + "]")

selection = int (input ("\nSelect a session (e.g. \"1\"): ")) - 1
session_href = sessions [selection].get ('href')

# Set selected session to 'active'
active_session ['href'] = sessions [selection].get ('href')
br.open (base_url + active_session ['href'])
br.open (browse_courses_url)

# Prompt user to select course
req.COURSE_SUBJECT_CODE = req.course_request ()

all_course_codes = br.find_all ("td")

for course_code in all_course_codes:
    if (len (course_code.findAll (text = True)) == 3):
        if (course_code.findAll (text = True) [1] == req.COURSE_SUBJECT_CODE):
            course_subj_req = course_code.find ('a') ['href']
            break

br.open (base_url + course_subj_req)
all_courses = br.find_all ("td")

req.COURSE_NUM = req.course_num_req ()
req.COURSE = req.COURSE_SUBJECT_CODE + " " + req.COURSE_NUM

for course in all_courses:
    if (course.findAll (text = True) [0] == req.COURSE):
        course_url = course.find ('a') ['href']

br.open (base_url + course_url)
sections = br.find_all ("td")

course_section = input ("Enter Course Section: ")

for section in sections:
    if (len (section.findAll (text = True)) == 3):
        section = section.findAll (text = True) [1].strip ()
        print (section)








#print ("SUCCESS!!!!")
#           print (req.SUBJECT_CODE)





#print (course.findAll (text = True))

#link = br.get_link (str (subject_code))



#print (link)


# Ask user




#

#print (active_session ['href'])###
#print (active_session['href']) #<a href="/cs/main?sessyr=2017&amp;sesscd=W" title="2017 Winter">2017 Winter</a>


#br.open (base_url + active_session ['href'])

#sess_num = re.search ('%s(.*)%s' % (start, end), str (table [2])).group (1)
#print (sess_num)


#active_session = sessions.findAll ('div', {"class" : "active" }).get ('href')

#print (active_session)
#sessions['href'] = sessions['href'].replace(active_session, sessions [selection].get ('href'))


#br.open(base_url + session_link)





#print (base_url + sessions [session].find ('href'))

#br.follow_link (base_url + sessions [session].find ('href'))

#browser.follow_link(songs[0])



#sessions = br.find_all ('div', {"class" : "pull-right"})[1].find_all ('div', {"class" : "btn-group"})[1]
#session = sessions.find_all ('a')[0]

#mydivs = soup.findAll("div", {"class": "stylelistrow"})

#print (session)



#from urllib.request import urlopen
#from bs4 import BeautifulSoup
#import datetime


#dept = input ("Enter course dept (e.g. PSYC): ")
#course_code = input ("Enter course code: ")
#url = "https://courses.students.ubc.ca/cs/main?pname=subjarea&tname=subjareas&req=3&dept=" + dept.upper() + "&course=" + course_code

#print (url)




#https://courses.students.ubc.ca/cs/main?pname=subjarea&tname=subjareas&req=3&dept=CPSC&course=310
#https://courses.students.ubc.ca/cs/main?pname=subjarea&tname=subjareas&req=3&dept=PSYC&course=101

