from typing import Any, Dict

class FederatedLoginRequest:
    def __init__(self, client_id: str, redirect_uri: str, scope: str, state: str):
        self.client_id = client_id
        self.redirect_uri = redirect_uri
        self.scope = scope
        self.state = state

    def to_dict(self) -> Dict[str, Any]:
        return {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'scope': self.scope,
            'state': self.state
        }


class FederatedLoginResponse:
    def __init__(self, code: str, state: str):
        self.code = code
        self.state = state

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(code=data['code'], state=data['state'])


def normalize_federated_login_response(response: Dict[str, Any]) -> FederatedLoginResponse:
    return FederatedLoginResponse.from_dict(response)