class OAuth2Token:
    def __init__(self, access_token, refresh_token, id_token, expires_in):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.id_token = id_token
        self.expires_in = expires_in