from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class TokenResponse:
    access_token: str
    token_type: str
    expires_in: int
    id_token: str | None = None
    refresh_token: str | None = None

    @classmethod
    def from_response(cls, data: Dict[str, Any]) -> 'TokenResponse':
        return cls(
            access_token=data['access_token'],
            token_type=data.get('token_type', 'Bearer'),
            expires_in=data.get('expires_in', 3600),
            id_token=data.get('id_token'),
            refresh_token=data.get('refresh_token'),
        )

@dataclass
class UserClaims:
    sub: str
    name: str | None = None
    given_name: str | None = None
    family_name: str | None = None
    email: str | None = None
    email_verified: bool | None = None
    picture: str | None = None

def normalize_claims(data: Dict[str, Any]) -> UserClaims:
    return UserClaims(
        sub=data['sub'],
        name=data.get('name'),
        given_name=data.get('given_name'),
        family_name=data.get('family_name'),
        email=data.get('email'),
        email_verified=data.get('email_verified'),
        picture=data.get('picture'),
    )
