from typing import Dict


class OAuth2TokenResponse:
    def __init__(self, access_token: str, refresh_token: str, expires_in: int):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.expires_in = expires_in

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(
            access_token=data["access_token"],
            refresh_token=data["refresh_token"],
            expires_in=data["expires_in"],
        )
