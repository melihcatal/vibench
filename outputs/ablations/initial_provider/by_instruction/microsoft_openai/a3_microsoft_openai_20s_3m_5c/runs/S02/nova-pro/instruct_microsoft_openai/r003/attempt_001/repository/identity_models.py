class AuthCodeFlow:
    def __init__(self, auth_uri):
        self.auth_uri = auth_uri

class TokenResponse:
    def __init__(self, access_token, id_token, expires_in):
        self.access_token = access_token
        self.id_token = id_token
        self.expires_in = expires_in