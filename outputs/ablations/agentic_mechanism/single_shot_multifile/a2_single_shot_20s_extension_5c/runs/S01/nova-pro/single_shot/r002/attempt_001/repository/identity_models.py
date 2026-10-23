class UserRegistration:
    def __init__(self, email, password):
        self.email = email
        self.password = password

class AuthTokens:
    def __init__(self, access_token, refresh_token):
        self.access_token = access_token
        self.refresh_token = refresh_token