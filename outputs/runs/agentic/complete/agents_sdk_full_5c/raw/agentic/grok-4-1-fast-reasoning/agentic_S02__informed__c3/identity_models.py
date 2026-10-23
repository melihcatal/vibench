from dataclasses import dataclass
from typing import Optional

@dataclass
class OauthToken:
    access_token: str
    token_type: str
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None

@dataclass
class UserProfile:
    sub: str
    email: Optional[str] = None
    name: Optional[str] = None
    picture: Optional[str] = None

def normalize_profile(raw: dict) -> UserProfile:
    return UserProfile(
        sub=raw.get('sub'),
        email=raw.get('email'),
        name=raw.get('name'),
        picture=raw.get('picture'),
    )