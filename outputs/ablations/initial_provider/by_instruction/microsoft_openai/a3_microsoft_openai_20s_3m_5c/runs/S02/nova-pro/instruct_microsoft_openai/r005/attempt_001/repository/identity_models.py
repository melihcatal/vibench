from typing import Dict

class AuthResponse:
    def __init__(self, access_token: str, id_token: str, refresh_token: str):
        self.access_token = access_token
        self.id_token = id_token
        self.refresh_token = refresh_token

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(data['access_token'], data['id_token'], data['refresh_token'])