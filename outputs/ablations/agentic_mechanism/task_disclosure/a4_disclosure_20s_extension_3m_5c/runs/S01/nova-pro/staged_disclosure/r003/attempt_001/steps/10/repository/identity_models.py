class EmailPasswordRequest:
    def __init__(self, email, password):
        self.email = email
        self.password = password

class EmailPasswordResponse:
    def __init__(self, status, message):
        self.status = status
        self.message = message

def normalize_email(email):
    return email.lower()

def normalize_password(password):
    return password