class UserRequest:
    def __init__(self, email, password):
        self.email = email
        self.password = password

class UserResponse:
    def __init__(self, user_id):
        self.user_id = user_id

class TokenRequest:
    def __init__(self, refresh_token):
        self.refresh_token = refresh_token

class TokenResponse:
    def __init__(self, access_token, refresh_token):
        self.access_token = access_token
        self.refresh_token = refresh_token