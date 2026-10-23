from typing import Dict


# Define local request, response, and normalization helpers for Federated Login Flow
class OAuthTokenResponse:
    def __init__(self, data: Dict):
        self.access_token = data.get("access_token")
        self.id_token = data.get("id_token")
        self.refresh_token = data.get("refresh_token")
