class OAuthResult:
    def __init__(self, access_token, id_token, refresh_token):
        self.access_token = access_token
        self.id_token = id_token
        self.refresh_token = refresh_token


class UserProfile:
    def __init__(self, user_id, email, name):
        self.user_id = user_id
        self.email = email
        self.name = name
