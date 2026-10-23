from typing import Dict


class OAuthResponse:
    def __init__(self, access_token: str, refresh_token: str, id_token: str):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.id_token = id_token


class UserProfile:
    def __init__(self, sub: str, name: str, email: str):
        self.sub = sub
        self.name = name
        self.email = email
