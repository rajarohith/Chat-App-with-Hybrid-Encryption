from werkzeug.security import check_password_hash
class ClassUser:
    def __init__(self, uname, em, pswd):
        self.username = uname
        self.email = em
        self.password = pswd
    @staticmethod
    def is_active():
        return True
    @staticmethod
    def is_anonymous():
        return False
    @staticmethod
    def is_authenticated():
        return True
    def check_password(self, password_input):
        return check_password_hash(self.password, password_input)
    def get_id(self):
        return self.username