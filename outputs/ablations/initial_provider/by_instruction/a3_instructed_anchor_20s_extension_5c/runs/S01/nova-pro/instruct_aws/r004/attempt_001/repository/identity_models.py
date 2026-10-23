class SignUpRequest:
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

class SignInRequest:
    def __init__(self, username, password):
        self.username = username
        self.password = password

class RefreshTokenRequest:
    def __init__(self, refresh_token):
        self.refresh_token = refresh_token

class ForgotPasswordRequest:
    def __init__(self, username):
        self.username = username