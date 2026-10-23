from typing import Dict, Any

class FederatedLoginRequest:
    def __init__(self, client_id: str, redirect_uri: str, scope: str, state: str):
        self.client_id = client_id
        self.redirect_uri = redirect_uri
        self.scope = scope
        self.state = state

    @staticmethod
    def normalize(request_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'client_id': request_data.get('client_id'),
            'redirect_uri': request_data.get('redirect_uri'),
            'scope': request_data.get('scope'),
            'state': request_data.get('state')
        }

class FederatedLoginResponse:
    def __init__(self, code: str, state: str):
        self.code = code
        self.state = state

    @staticmethod
    def normalize(response_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'code': response_data.get('code'),
            'state': response_data.get('state')
        }

class FederatedLoginError:
    def __init__(self, error: str, error_description: str, state: str):
        self.error = error
        self.error_description = error_description
        self.state = state

    @staticmethod
    def normalize(error_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'error': error_data.get('error'),
            'error_description': error_data.get('error_description'),
            'state': error_data.get('state')
        }