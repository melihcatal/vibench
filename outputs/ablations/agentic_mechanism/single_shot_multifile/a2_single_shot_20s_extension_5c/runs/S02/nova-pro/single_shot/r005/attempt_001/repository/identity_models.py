from typing import Dict

class OAuthTokenResponse:
    def __init__(self, access_token: str, id_token: str, refresh_token: str):
        self.access_token = access_token
        self.id_token = id_token
        self.refresh_token = refresh_token

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(
            access_token=data['access_token'],
            id_token=data['id_token'],
            refresh_token=data['refresh_token']
        )

class UserProfile:
    def __init__(self, sub: str, email: str, name: str):
        self.sub = sub
        self.email = email
        self.name = name

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(
            sub=data['sub'],
            email=data['email'],
            name=data['name']
        )