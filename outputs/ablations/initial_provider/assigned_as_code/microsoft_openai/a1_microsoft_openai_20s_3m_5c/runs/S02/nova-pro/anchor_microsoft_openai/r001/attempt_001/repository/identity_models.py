class OAuth2Request:
    def __init__(self, scopes, redirect_uri):
        self.scopes = scopes
        self.redirect_uri = redirect_uri


class OAuth2Response:
    def __init__(self, access_token, id_token, refresh_token):
        self.access_token = access_token
        self.id_token = id_token
        self.refresh_token = refresh_token