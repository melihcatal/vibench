class OAuthToken:
    def __init__(self, access_token, refresh_token, expires_in):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.expires_in = expires_in

class UserProfile:
    def __init__(self, user_id, email, name):
        self.user_id = user_id
        self.email = email
        self.name = name