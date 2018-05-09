from flask_login import UserMixin
from app import login

class User (UserMixin):
    def __init__(self, id):
        self.id = id

@login.user_loader
def load_user (id):
    return User (id=id)
