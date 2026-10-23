from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List
from datetime import datetime
import json


@dataclass
class AuthRequest:
    state: str
    nonce: Optional[str] = None
    code_verifier: Optional[str] = None
    code_challenge: Optional[str] = None
    code_challenge_method: Optional[str] = None
    redirect_uri: Optional[str] = None
    scopes: List[str] = field(default_factory=lambda: ["openid", "profile", "email"])
    provider: str = "auth0"
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "state": self.state,
            "nonce": self.nonce,
            "code_verifier": self.code_verifier,
            "code_challenge": self.code_challenge,
            "code_challenge_method": self.code_challenge_method,
            "redirect_uri": self.redirect_uri,
            "scopes": self.scopes,
            "provider": self.provider,
            "timestamp": self.timestamp.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AuthRequest":
        return cls(
            state=data["state"],
            nonce=data.get("nonce"),
            code_verifier=data.get("code_verifier"),
            code_challenge=data.get("code_challenge"),
            code_challenge_method=data.get("code_challenge_method"),
            redirect_uri=data.get("redirect_uri"),
            scopes=data.get("scopes", ["openid", "profile", "email"]),
            provider=data.get("provider", "auth0"),
            timestamp=datetime.fromisoformat(data["timestamp"])
            if "timestamp" in data
            else datetime.now(),
        )


@dataclass
class TokenResponse:
    access_token: str
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    expires_in: Optional[int] = None
    token_type: str = "Bearer"
    scope: Optional[str] = None
    provider: str = "auth0"
    received_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "access_token": self.access_token,
            "id_token": self.id_token,
            "refresh_token": self.refresh_token,
            "expires_in": self.expires_in,
            "token_type": self.token_type,
            "scope": self.scope,
            "provider": self.provider,
            "received_at": self.received_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TokenResponse":
        return cls(
            access_token=data["access_token"],
            id_token=data.get("id_token"),
            refresh_token=data.get("refresh_token"),
            expires_in=data.get("expires_in"),
            token_type=data.get("token_type", "Bearer"),
            scope=data.get("scope"),
            provider=data.get("provider", "auth0"),
            received_at=datetime.fromisoformat(data["received_at"])
            if "received_at" in data
            else datetime.now(),
        )


@dataclass
class UserProfile:
    user_id: str
    email: Optional[str] = None
    email_verified: bool = False
    name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    nickname: Optional[str] = None
    picture: Optional[str] = None
    locale: Optional[str] = None
    updated_at: Optional[str] = None
    provider: str = "auth0"
    raw_claims: Dict[str, Any] = field(default_factory=dict)

    def to_normalized_dict(self) -> Dict[str, Any]:
        return {
            "id": self.user_id,
            "email": self.email,
            "email_verified": self.email_verified,
            "full_name": self.name,
            "first_name": self.given_name,
            "last_name": self.family_name,
            "display_name": self.nickname or self.name,
            "avatar_url": self.picture,
            "locale": self.locale,
            "last_updated": self.updated_at,
            "provider": self.provider,
        }

    @classmethod
    def from_claims(
        cls, claims: Dict[str, Any], provider: str = "auth0"
    ) -> "UserProfile":
        user_id = claims.get("sub") or claims.get("user_id") or claims.get("oid")

        return cls(
            user_id=user_id,
            email=claims.get("email"),
            email_verified=claims.get("email_verified", False),
            name=claims.get("name"),
            given_name=claims.get("given_name"),
            family_name=claims.get("family_name"),
            nickname=claims.get("nickname"),
            picture=claims.get("picture"),
            locale=claims.get("locale"),
            updated_at=claims.get("updated_at"),
            provider=provider,
            raw_claims=claims,
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "email": self.email,
            "email_verified": self.email_verified,
            "name": self.name,
            "given_name": self.given_name,
            "family_name": self.family_name,
            "nickname": self.nickname,
            "picture": self.picture,
            "locale": self.locale,
            "updated_at": self.updated_at,
            "provider": self.provider,
            "raw_claims": self.raw_claims,
        }


@dataclass
class AuthError:
    error: str
    error_description: Optional[str] = None
    error_uri: Optional[str] = None
    state: Optional[str] = None
    provider: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "error": self.error,
            "error_description": self.error_description,
            "error_uri": self.error_uri,
            "state": self.state,
            "provider": self.provider,
            "timestamp": self.timestamp.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AuthError":
        return cls(
            error=data["error"],
            error_description=data.get("error_description"),
            error_uri=data.get("error_uri"),
            state=data.get("state"),
            provider=data.get("provider"),
            timestamp=datetime.fromisoformat(data["timestamp"])
            if "timestamp" in data
            else datetime.now(),
        )


def normalize_provider_claims(claims: Dict[str, Any], provider: str) -> Dict[str, Any]:
    normalized = {}

    if provider == "auth0":
        normalized = {
            "sub": claims.get("sub"),
            "email": claims.get("email"),
            "email_verified": claims.get("email_verified", False),
            "name": claims.get("name"),
            "given_name": claims.get("given_name"),
            "family_name": claims.get("family_name"),
            "nickname": claims.get("nickname"),
            "picture": claims.get("picture"),
            "locale": claims.get("locale"),
            "updated_at": claims.get("updated_at"),
        }
    elif provider == "cognito":
        normalized = {
            "sub": claims.get("sub"),
            "email": claims.get("email"),
            "email_verified": claims.get("email_verified", False),
            "name": claims.get("name"),
            "given_name": claims.get("given_name"),
            "family_name": claims.get("family_name"),
            "nickname": claims.get("nickname"),
            "picture": claims.get("picture"),
            "locale": claims.get("locale"),
        }
    elif provider == "azure":
        normalized = {
            "sub": claims.get("sub") or claims.get("oid"),
            "email": claims.get("email") or claims.get("preferred_username"),
            "email_verified": claims.get("email_verified", False),
            "name": claims.get("name"),
            "given_name": claims.get("given_name"),
            "family_name": claims.get("family_name"),
            "picture": None,
            "locale": claims.get("locale"),
        }

    normalized["provider"] = provider
    normalized["raw_claims"] = claims

    return normalized
