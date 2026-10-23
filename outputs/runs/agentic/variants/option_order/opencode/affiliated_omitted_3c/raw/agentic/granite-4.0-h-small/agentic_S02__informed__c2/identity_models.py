from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class UserProfile:
    sub: str
    name: str = ''
    email: str = ''
    picture: str = ''
    locale: str = ''
    # Add any other normalized claims as needed

    @classmethod
def from_dict(cls, data: Dict[str, Any]):
        return cls(**data)

@dataclass
class OAuth2TokenResponse:
    access_token: str = ''
    refresh_token: str = ''
    id_token: str = ''
    # Add further fields as needed

@classmethod
def from_dict(cls, data: Dict[str, Any]):
    return cls(**data)
