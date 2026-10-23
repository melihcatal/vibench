class OAuthTokenResponse:
    def __init__(self, access_token, token_type, expires_in, scope):
        self.access_token = access_token
        self.token_type = token_type
        self.expires_in = expires_in
        self.scope = scope

class UserProfile:
    def __init__(self, sub, name, email):
        self.sub = sub
        self.name = name
        self.email = email