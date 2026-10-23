class OAuthTokenResponse:
    def __init__(self, access_token, token_type, expires_in, id_token, refresh_token):
        self.access_token = access_token
        self.token_type = token_type
        self.expires_in = expires_in
        self.id_token = id_token
        self.refresh_token = refresh_token

class UserProfile:
    def __init__(self, sub, name, given_name, family_name, email):
        self.sub = sub
        self.name = name
        self.given_name = given_name
        self.family_name = family_name
        self.email = email
