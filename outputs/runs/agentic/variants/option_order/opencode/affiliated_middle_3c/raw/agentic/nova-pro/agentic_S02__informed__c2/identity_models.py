# [HELPER] identity_models.py
# Define local request, response, and normalization helpers for Federated Login Flow
class OAuthResponse:
    def __init__(self, access_token, refresh_token, id_token, expires_in):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.id_token = id_token
        self.expires_in = expires_in


class UserProfile:
    def __init__(self, user_id, email, name):
        self.user_id = user_id
        self.email = email
        self.name = name
