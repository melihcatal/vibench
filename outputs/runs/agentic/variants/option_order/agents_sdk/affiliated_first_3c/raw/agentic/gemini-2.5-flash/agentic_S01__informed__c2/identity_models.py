class UserRegistrationRequest:
    def __init__(self, email, password):
        self.email = email
        self.password = password

class UserRegistrationResponse:
    def __init__(self, uid, email):
        self.uid = uid
        self.email = email

class UserLoginRequest:
    def __init__(self, email, password):
        self.email = email
        self.password = password

class UserLoginResponse:
    def __init__(self, uid, email, custom_token=None):
        self.uid = uid
        self.email = email
        self.custom_token = custom_token # Custom token from Firebase Admin SDK

class RefreshSessionRequest:
    def __init__(self, id_token):
        self.id_token = id_token

class RefreshSessionResponse:
    def __init__(self, uid, email, message):
        self.uid = uid
        self.email = email
        self.message = message

class PasswordResetRequest:
    def __init__(self, email):
        self.email = email

class PasswordResetResponse:
    def __init__(self, email, message):
        self.email = email
        self.message = message
