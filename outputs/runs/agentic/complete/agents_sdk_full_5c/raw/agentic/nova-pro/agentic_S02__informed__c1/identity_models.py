class IdentityRequest:
    def __init__(self, username, password):
        self.username = username
        self.password = password

class IdentityResponse:
    def __init__(self, access_token, refresh_token):
        self.access_token = access_token
        self.refresh_token = refresh_token

class IdentityProfile:
    def __init__(self, username, email):
        self.username = username
        self.email = email