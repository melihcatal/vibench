from dataclasses import dataclass
import json

@dataclass
class TokenResponse:
    access_token: str
    refresh_token: str = None
    id_token: str = None
    expires_in: int = None
    token_type: str = "Bearer"

@dataclass
class UserInfo:
    sub: str
    email: str = None
    email_verified: bool = False
    name: str = None
    given_name: str = None
    family_name: str = None
    picture: str = None
    locale: str = None
    provider: str = None

def normalize_google_user_info(raw_info: dict) -> UserInfo:
    return UserInfo(
        sub=raw_info.get("sub"),
        email=raw_info.get("email"),
        email_verified=raw_info.get("email_verified", False),
        name=raw_info.get("name"),
        given_name=raw_info.get("given_name"),
        family_name=raw_info.get("family_name"),
        picture=raw_info.get("picture"),
        locale=raw_info.get("locale"),
        provider="google"
    )

def normalize_auth0_user_info(raw_info: dict) -> UserInfo:
    return UserInfo(
        sub=raw_info.get("sub"),
        email=raw_info.get("email"),
        email_verified=raw_info.get("email_verified", False),
        name=raw_info.get("name"),
        given_name=raw_info.get("given_name"),
        family_name=raw_info.get("family_name"),
        picture=raw_info.get("picture"),
        locale=raw_info.get("locale"),
        provider="auth0"
    )
