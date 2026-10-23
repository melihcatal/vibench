class User:
    def __init__(self, email, password):
        self.email = email
        self.password = password

class AuthResponse:
    def __init__(self, token):
        self.token = token