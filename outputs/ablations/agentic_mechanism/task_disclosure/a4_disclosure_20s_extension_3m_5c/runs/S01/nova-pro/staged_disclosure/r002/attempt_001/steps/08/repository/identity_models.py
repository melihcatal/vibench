class EmailPasswordAccountRequest:
    def __init__(self, email, password):
        self.email = email
        self.password = password

class EmailPasswordAccountResponse:
    def __init__(self, success, message):
        self.success = success
        self.message = message

def normalize_email(email):
    return email.lower()

def normalize_password(password):
    return password