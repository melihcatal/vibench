from typing import Any, Dict


class FederatedLoginRequest:
    def __init__(self, client_id: str, redirect_uri: str, scope: str):
        self.client_id = client_id
        self.redirect_uri = redirect_uri
        self.scope = scope

    def to_dict(self) -> Dict[str, Any]:
        return {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'scope': self.scope
        }


class FederatedLoginResponse:
    def __init__(self, access_token: str, token_type: str, expires_in: int):
        self.access_token = access_token
        self.token_type = token_type
        self.expires_in = expires_in

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(
            access_token=data['access_token'],
            token_type=data['token_type'],
            expires_in=data['expires_in']
        )


def normalize_federated_login_response(response: Dict[str, Any]) -> FederatedLoginResponse:
    return FederatedLoginResponse.from_dict(response)