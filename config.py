import os
import getpass

def cls(): os.system('cls' if os.name=='nt' else 'clear')

DATACOUP_USERNAME = input ("Enter CWL id: ")
DATACOUP_PASSWORD = getpass.getpass ("Enter CWL password: ")
DATACOUP_MOBILE = input ("Enter your phone number: ")
