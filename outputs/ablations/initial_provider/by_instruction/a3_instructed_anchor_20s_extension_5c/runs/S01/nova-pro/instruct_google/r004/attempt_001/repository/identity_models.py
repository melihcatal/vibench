class RegisterUserRequest:
    def __init__(self, email, password):
        self.email = email
        self.password = password

class RegisterUserResponse:
    def __init__(self, idToken, email, refreshToken):
        self.idToken = idToken
        self.email = email
        self.refreshToken = refreshToken

class LoginRequest:
    def __init__(self, email, password):
        self.email = email
        self.password = password

class LoginResponse:
    def __init__(self, idToken, email, refreshToken):
        self.idToken = idToken
        self.email = email
        self.refreshToken = refreshToken