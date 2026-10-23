class RegisterUserRequest:
    def __init__(self, email, password):
        self.email = email
        self.password = password

class LoginRequest:
    def __init__(self, email, password):
        self.email = email
        self.password = password

class PasswordResetRequest:
    def __init__(self, email):
        self.email = email