from typing import Dict

# Define local request, response, and normalization helpers for Federated Login Flow


class OAuthTokenResponse:
    def __init__(self, access_token: str, id_token: str, refresh_token: str):
        self.access_token = access_token
        self.id_token = id_token
        self.refresh_token = refresh_token


class UserProfile:
    def __init__(self, sub: str, name: str):
        self.sub = sub
        self.name = name


def normalize_id_token(id_token: Dict) -> UserProfile:
    return UserProfile(id_token["sub"], id_token["name"])
