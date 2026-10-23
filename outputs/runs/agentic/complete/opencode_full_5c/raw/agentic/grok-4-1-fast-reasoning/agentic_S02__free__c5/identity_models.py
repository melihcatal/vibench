from dataclasses import dataclass
from typing import Any, Optional
from datetime import datetime


@dataclass
class OAuthTokens:
    access_token: str
    token_type: str
    expires_in: int
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None


@dataclass
class UserProfile:
    sub: str
    email: Optional[str] = None
    name: Optional[str] = None
    picture: Optional[str] = None


@dataclass
class AuditEvent:
    timestamp: datetime
    event_type: str
    user_id: Optional[str] = None
    details: dict[str, Any] = None


def parse_oauth_response(data: dict[str, Any]) -> OAuthTokens:
    return OAuthTokens(
        access_token=data["access_token"],
        token_type=data["token_type"],
        expires_in=data["expires_in"],
        id_token=data.get("id_token"),
        refresh_token=data.get("refresh_token"),
    )


def parse_userinfo_response(data: dict[str, Any]) -> UserProfile:
    return UserProfile(
        sub=data["sub"],
        email=data.get("email"),
        name=data.get("name"),
        picture=data.get("picture"),
    )
