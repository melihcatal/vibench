class OAuthResponse:
    def __init__(self, code):
        self.code = code

class TokenResponse:
    def __init__(self, access_token, refresh_token):
        self.access_token = access_token
        self.refresh_token = refresh_token