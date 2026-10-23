class OAuthCallbackResponse:
    def __init__(self, access_token, id_token, refresh_token, expires_in, token_type):
        self.access_token = access_token
        self.id_token = id_token
        self.refresh_token = refresh_token
        self.expires_in = expires_in
        self.token_type = token_type


class UserProfile:
    def __init__(self, sub, email, name):
        self.sub = sub
        self.email = email
        self.name = name