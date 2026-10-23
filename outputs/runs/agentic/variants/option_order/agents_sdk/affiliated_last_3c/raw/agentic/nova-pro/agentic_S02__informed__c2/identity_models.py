class OAuthTokenResponse:
    def __init__(self, access_token, token_type, expires_in, scope, refresh_token=None):
        self.access_token = access_token
        self.token_type = token_type
        self.expires_in = expires_in
        self.scope = scope
        self.refresh_token = refresh_token

class UserProfile:
    def __init__(self, user_id, name, email):
        self.user_id = user_id
        self.name = name
        self.email = email