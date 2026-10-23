from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from enum import Enum


class LoginProvider(Enum):
    AUTH0 = "auth0"
    OKTA = "okta"
    GOOGLE = "google"
    MICROSOFT = "microsoft"


@dataclass
class OAuthTokenResponse:
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: Optional[str] = None
    scope: Optional[str] = None
    id_token: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class NormalizedProfile:
    sub: str
    name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    email: Optional[str] = None
    email_verified: bool = False
    picture: Optional[str] = None
    locale: Optional[str] = None
    updated_at: Optional[str] = None
    nickname: Optional[str] = None
    custom_claims: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class LoginAuditEvent:
    user_id: str
    provider: LoginProvider
    event_type: str
    timestamp: str
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["provider"] = self.provider.value
        return data
