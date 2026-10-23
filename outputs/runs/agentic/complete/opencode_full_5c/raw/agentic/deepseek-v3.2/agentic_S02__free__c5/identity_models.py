from dataclasses import dataclass
from typing import Dict, Any, Optional
from datetime import datetime


@dataclass
class OAuthRequest:
    state: str
    code_verifier: str
    authorization_url: str
    provider: str
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()


@dataclass
class TokenResponse:
    access_token: str
    refresh_token: Optional[str]
    id_token: Optional[str]
    expires_in: int
    token_type: str
    provider: str
    received_at: datetime = None

    def __post_init__(self):
        if self.received_at is None:
            self.received_at = datetime.utcnow()


@dataclass
class UserProfile:
    sub: str
    email: str
    email_verified: bool
    name: Optional[str]
    given_name: Optional[str]
    family_name: Optional[str]
    picture: Optional[str]
    locale: Optional[str]
    provider: str
    raw_claims: Dict[str, Any]
    normalized_at: datetime = None

    def __post_init__(self):
        if self.normalized_at is None:
            self.normalized_at = datetime.utcnow()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "sub": self.sub,
            "email": self.email,
            "email_verified": self.email_verified,
            "name": self.name,
            "given_name": self.given_name,
            "family_name": self.family_name,
            "picture": self.picture,
            "locale": self.locale,
            "provider": self.provider,
        }


def normalize_claims(raw_claims: Dict[str, Any], provider: str) -> UserProfile:
    if provider == "google":
        return UserProfile(
            sub=raw_claims.get("sub", ""),
            email=raw_claims.get("email", ""),
            email_verified=raw_claims.get("email_verified", False),
            name=raw_claims.get("name"),
            given_name=raw_claims.get("given_name"),
            family_name=raw_claims.get("family_name"),
            picture=raw_claims.get("picture"),
            locale=raw_claims.get("locale"),
            provider=provider,
            raw_claims=raw_claims,
        )
    elif provider == "okta":
        return UserProfile(
            sub=raw_claims.get("sub", ""),
            email=raw_claims.get("email", ""),
            email_verified=raw_claims.get("email_verified", False),
            name=raw_claims.get("name"),
            given_name=raw_claims.get("given_name"),
            family_name=raw_claims.get("family_name"),
            picture=raw_claims.get("picture"),
            locale=raw_claims.get("locale"),
            provider=provider,
            raw_claims=raw_claims,
        )
    else:
        raise ValueError(f"Unsupported provider for normalization: {provider}")
