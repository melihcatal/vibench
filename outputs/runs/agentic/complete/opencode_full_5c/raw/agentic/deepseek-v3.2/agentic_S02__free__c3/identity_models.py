from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List
from datetime import datetime
import json


@dataclass
class OAuthRequest:
    provider: str
    state: str
    nonce: str
    redirect_uri: str
    scope: str
    code_challenge: Optional[str] = None
    code_challenge_method: Optional[str] = None
    prompt: str = "login"

    def to_dict(self) -> Dict[str, Any]:
        data = {
            "provider": self.provider,
            "state": self.state,
            "nonce": self.nonce,
            "redirect_uri": self.redirect_uri,
            "scope": self.scope,
            "prompt": self.prompt,
        }
        if self.code_challenge:
            data["code_challenge"] = self.code_challenge
            data["code_challenge_method"] = self.code_challenge_method
        return data


@dataclass
class TokenResponse:
    access_token: str
    token_type: str
    expires_in: int
    scope: str
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    provider: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any], provider: str = None) -> "TokenResponse":
        return cls(
            access_token=data.get("access_token", ""),
            token_type=data.get("token_type", "Bearer"),
            expires_in=data.get("expires_in", 3600),
            scope=data.get("scope", ""),
            id_token=data.get("id_token"),
            refresh_token=data.get("refresh_token"),
            provider=provider,
        )

    def is_valid(self) -> bool:
        return bool(self.access_token and self.token_type)


@dataclass
class UserProfile:
    sub: str
    email: str
    email_verified: bool
    name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    picture: Optional[str] = None
    locale: Optional[str] = None
    provider: Optional[str] = None
    raw_claims: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_google_claims(cls, claims: Dict[str, Any]) -> "UserProfile":
        return cls(
            sub=claims.get("sub", ""),
            email=claims.get("email", ""),
            email_verified=claims.get("email_verified", False),
            name=claims.get("name"),
            given_name=claims.get("given_name"),
            family_name=claims.get("family_name"),
            picture=claims.get("picture"),
            locale=claims.get("locale"),
            provider="google",
            raw_claims=claims,
        )

    @classmethod
    def from_okta_claims(cls, claims: Dict[str, Any]) -> "UserProfile":
        return cls(
            sub=claims.get("sub", ""),
            email=claims.get("email", ""),
            email_verified=claims.get("email_verified", False),
            name=claims.get("name"),
            given_name=claims.get("given_name"),
            family_name=claims.get("family_name"),
            picture=claims.get("picture"),
            locale=claims.get("locale"),
            provider="okta",
            raw_claims=claims,
        )

    def normalize(self) -> Dict[str, Any]:
        normalized = {
            "id": self.sub,
            "email": self.email,
            "email_verified": self.email_verified,
            "full_name": self.name,
            "first_name": self.given_name,
            "last_name": self.family_name,
            "avatar_url": self.picture,
            "locale": self.locale,
            "provider": self.provider,
        }
        return {k: v for k, v in normalized.items() if v is not None}

    def to_json(self) -> str:
        return json.dumps(self.normalize(), indent=2)


@dataclass
class AuthSession:
    session_id: str
    user_id: Optional[str] = None
    provider: Optional[str] = None
    access_token: Optional[str] = None
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    expires_at: Optional[datetime] = None
    claims: Optional[Dict[str, Any]] = None

    def is_valid(self) -> bool:
        if not self.access_token:
            return False
        if self.expires_at and datetime.now() > self.expires_at:
            return False
        return True

    def to_dict(self) -> Dict[str, Any]:
        data = {
            "session_id": self.session_id,
            "user_id": self.user_id,
            "provider": self.provider,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "has_claims": bool(self.claims),
        }
        return data


def normalize_provider_claims(claims: Dict[str, Any], provider: str) -> Dict[str, Any]:
    normalizers = {
        "google": UserProfile.from_google_claims,
        "okta": UserProfile.from_okta_claims,
    }

    if provider not in normalizers:
        return claims

    profile = normalizers[provider](claims)
    return profile.normalize()
