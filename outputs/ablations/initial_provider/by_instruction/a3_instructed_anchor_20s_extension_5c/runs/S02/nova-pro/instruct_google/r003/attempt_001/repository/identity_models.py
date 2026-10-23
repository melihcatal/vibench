class OAuth2Request:
    def __init__(self, scopes):
        self.scopes = scopes

class OAuth2Response:
    def __init__(self, access_token, refresh_token):
        self.access_token = access_token
        self.refresh_token = refresh_token