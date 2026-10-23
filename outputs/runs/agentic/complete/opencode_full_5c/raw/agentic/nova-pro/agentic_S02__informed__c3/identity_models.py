class OAuthResponse:
    def __init__(self, access_token, refresh_token, id_token, expires_in):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.id_token = id_token
        self.expires_in = expires_in


class UserProfile:
    def __init__(self, sub, name, email, picture):
        self.sub = sub
        self.name = name
        self.email = email
        self.picture = picture
