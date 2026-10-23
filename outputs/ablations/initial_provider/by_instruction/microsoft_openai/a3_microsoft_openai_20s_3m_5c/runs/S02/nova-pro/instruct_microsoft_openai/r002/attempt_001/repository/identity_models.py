from typing import Dict

class AuthCodeFlow:
    def __init__(self, auth_uri: str):
        self.auth_uri = auth_uri

class TokenResponse:
    def __init__(self, access_token: str, id_token: str, refresh_token: str):
        self.access_token = access_token
        self.id_token = id_token
        self.refresh_token = refresh_token

class ProfileClaims:
    def __init__(self, claims: Dict):
        self.claims = claims