class RegisterUserRequest:
    def __init__(self, email, password):
        self.email = email
        self.password = password


class RegisterUserResponse:
    def __init__(self, token):
        self.token = token


class LoginRequest:
    def __init__(self, email, password):
        self.email = email
        self.password = password


class LoginResponse:
    def __init__(self, token):
        self.token = token


class RefreshSessionRequest:
    def __init__(self, refresh_token):
        self.refresh_token = refresh_token


class RefreshSessionResponse:
    def __init__(self, token):
        self.token = token


class PasswordResetRequest:
    def __init__(self, email):
        self.email = email


class PasswordResetResponse:
    def __init__(self, response):
        self.response = response
