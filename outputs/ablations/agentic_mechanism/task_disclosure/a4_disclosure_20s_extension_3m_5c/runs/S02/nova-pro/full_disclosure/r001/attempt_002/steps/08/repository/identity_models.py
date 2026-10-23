from typing import Dict, Any

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
    def __init__(self, authorization_code: str, state: str):
        self.authorization_code = authorization_code
        self.state = state

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'FederatedLoginResponse':
        return FederatedLoginResponse(data['authorization_code'], data['state'])

def normalize_federated_login_response(response: FederatedLoginResponse) -> Dict[str, Any]:
    return {
        'authorization_code': response.authorization_code,
        'state': response.state
    }