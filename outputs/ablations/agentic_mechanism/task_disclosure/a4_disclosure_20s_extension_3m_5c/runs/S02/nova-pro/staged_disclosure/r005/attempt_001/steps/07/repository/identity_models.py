from typing import Any, Dict, Union


class FederatedLoginRequest:
    def __init__(self, provider: str, redirect_uri: str, state: str, scope: str):
        self.provider = provider
        self.redirect_uri = redirect_uri
        self.state = state
        self.scope = scope


class FederatedLoginResponse:
    def __init__(self, access_token: str, id_token: str, expires_in: int):
        self.access_token = access_token
        self.id_token = id_token
        self.expires_in = expires_in


def normalize_id_token(id_token: str) -> Dict[str, Any]:
    # Placeholder for actual normalization logic
    return {'sub': 'user_id', 'name': 'User Name'}


def normalize_access_token(access_token: str) -> Dict[str, Any]:
    # Placeholder for actual normalization logic
    return {'provider': 'example_provider', 'scope': 'example_scope'}