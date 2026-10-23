class OAuth2Token:
    def __init__(self, access_token, refresh_token, token_uri, client_id, client_secret, scopes):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.token_uri = token_uri
        self.client_id = client_id
        self.client_secret = client_secret
        self.scopes = scopes