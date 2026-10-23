class OAuthTokenResponse:
    def __init__(self, access_token, id_token, refresh_token, expires_in):
        self.access_token = access_token
        self.id_token = id_token
        self.refresh_token = refresh_token
        self.expires_in = expires_in
