from robobrowser import RoboBrowser

login_portal = "https://cas.id.ubc.ca/ubc-cas/login?TARGET=https%3A%2F%2Fcourses.students.ubc.ca%2Fcs%2Fsecure%2Flogin%3FIMGSUBMIT.x%3D50%26IMGSUBMIT.y%3D18%26IMGSUBMIT%3DIMGSUBMIT"
base_url = "https://courses.students.ubc.ca"
browse_url = base_url + "/cs/main?pname=subjarea&tname=subjareas&req=0"

def get_sessions ():
    br = RoboBrowser (parser = 'html.parser')
    br.open ('https://courses.students.ubc.ca/cs/main?newSession=true')
    sessions = br.select ('a[href^="/cs/main?sessyr="]')
    choices = []
    for session in sessions:
        choices.append (''.join (session.findAll (text = True)))
    return choices


