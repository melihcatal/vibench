from typing import Dict


class OAuthCallbackResponse:
    def __init__(self, access_token: str, refresh_token: str):
        self.access_token = access_token
        self.refresh_token = refresh_token


class ProfileClaimsResponse:
    def __init__(self, email: str, name: str, picture: str):
        self.email = email
        self.name = name
        self.picture = picture


class PKCELoginResponse:
    def __init__(self, authorization_url: str, session_id: str, code_verifier: str):
        self.authorization_url = authorization_url
        self.session_id = session_id
        self.code_verifier = code_verifier