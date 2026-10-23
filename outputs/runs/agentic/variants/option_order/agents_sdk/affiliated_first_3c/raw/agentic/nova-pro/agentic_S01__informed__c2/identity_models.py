class SignUpRequest:
    def __init__(self, email, password):
        self.email = email
        self.password = password

class SignInRequest:
    def __init__(self, email, password):
        self.email = email
        self.password = password

class RefreshTokenRequest:
    def __init__(self, refresh_token):
        self.refresh_token = refresh_token

class PasswordResetRequest:
    def __init__(self, email):
        self.email = email