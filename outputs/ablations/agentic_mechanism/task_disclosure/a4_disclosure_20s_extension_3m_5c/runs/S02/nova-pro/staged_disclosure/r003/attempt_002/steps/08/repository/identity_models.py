from typing import Any, Dict, Optional


class FederatedLoginRequest:
    def __init__(self, provider: str, redirect_uri: str, state: Optional[str] = None):
        self.provider = provider
        self.redirect_uri = redirect_uri
        self.state = state

    def to_dict(self) -> Dict[str, Any]:
        return {
            'provider': self.provider,
            'redirect_uri': self.redirect_uri,
            'state': self.state
        }


class FederatedLoginResponse:
    def __init__(self, access_token: str, id_token: str, expires_in: int):
        self.access_token = access_token
        self.id_token = id_token
        self.expires_in = expires_in

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(
            access_token=data['access_token'],
            id_token=data['id_token'],
            expires_in=data['expires_in']
        )


def normalize_federated_login_response(response: Dict[str, Any]) -> FederatedLoginResponse:
    return FederatedLoginResponse.from_dict(response)