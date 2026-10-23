class UserLoginRequest:
    def __init__(self, email, password):
        self.email = email
        self.password = password

class UserLoginResponse:
    def __init__(self, id_token, refresh_token, uid):
        self.id_token = id_token
        self.refresh_token = refresh_token
        self.uid = uid

class PasswordResetRequest:
    def __init__(self, email):
        self.email = email
