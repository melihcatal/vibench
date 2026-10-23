from typing import Dict


class AuthorizationRequest:
    def __init__(self, client_id: str, redirect_uri: str, scope: str, state: str):
        self.client_id = client_id
        self.redirect_uri = redirect_uri
        self.scope = scope
        self.state = state


class AuthorizationResponse:
    def __init__(self, code: str, state: str):
        self.code = code
        self.state = state


class TokenRequest:
    def __init__(
        self, client_id: str, client_secret: str, code: str, redirect_uri: str
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.code = code
        self.redirect_uri = redirect_uri


class TokenResponse:
    def __init__(self, access_token: str, id_token: str, refresh_token: str):
        self.access_token = access_token
        self.id_token = id_token
        self.refresh_token = refresh_token


class UserProfile:
    def __init__(self, sub: str, name: str, email: str):
        self.sub = sub
        self.name = name
        self.email = email


def normalize_profile(profile: Dict):
    return UserProfile(
        sub=profile.get("sub"), name=profile.get("name"), email=profile.get("email")
    )
