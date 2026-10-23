from typing import Dict, Any

class OAuthResponse:
    def __init__(self, data: Dict[str, Any]):
        self.data = data

    @property
    def access_token(self):
        return self.data.get('AuthenticationResult', {}).get('AccessToken')

    @property
    def id_token(self):
        return self.data.get('AuthenticationResult', {}).get('IdToken')

    @property
    def refresh_token(self):
        return self.data.get('AuthenticationResult', {}).get('RefreshToken')