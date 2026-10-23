class RegisterUserRequest:
    def __init__(self, email, password):
        self.email = email
        self.password = password

class LoginRequest:
    def __init__(self, email, password):
        self.email = email
        self.password = password

class RefreshSessionRequest:
    def __init__(self, refresh_token):
        self.refresh_token = refresh_token

class PasswordResetRequest:
    def __init__(self, email):
        self.email = email

class AuthResponse:
    def __init__(self, id_token, access_token, refresh_token, expires_in):
        self.id_token = id_token
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.expires_in = expires_in
