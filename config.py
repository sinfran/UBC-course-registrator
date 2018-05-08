import os
import getpass

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

def cls(): os.system('cls' if os.name=='nt' else 'clear')

cls ()
DATACOUP_USERNAME = input ("Enter CWL id: ")
DATACOUP_PASSWORD = getpass.getpass ("Enter CWL password: ")
DATACOUP_MOBILE = input ("Enter your phone number: ")
