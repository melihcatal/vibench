from typing import Any, Dict


class OAuthRequest:
    def __init__(self, redirect_uri: str, state: str):
        self.redirect_uri = redirect_uri
        self.state = state


class OAuthResponse:
    def __init__(self, access_token: str, id_token: str, expires_in: int):
        self.access_token = access_token
        self.id_token = id_token
        self.expires_in = expires_in


class ProfileClaims:
    def __init__(self, sub: str, name: str, email: str):
        self.sub = sub
        self.name = name
        self.email = email


def normalize_profile_claims(claims: Dict[str, Any]) -> ProfileClaims:
    return ProfileClaims(
        sub=claims.get("sub", ""),
        name=claims.get("name", ""),
        email=claims.get("email", ""),
    )
