from dataclasses import dataclass
from typing import Dict, Any, Optional, List
from datetime import datetime
import json


@dataclass
class TokenResponse:
    id_token: Optional[str]
    access_token: str
    refresh_token: Optional[str]
    expires_in: int
    token_type: str
    scope: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TokenResponse":
        return cls(
            id_token=data.get("id_token"),
            access_token=data["access_token"],
            refresh_token=data.get("refresh_token"),
            expires_in=data["expires_in"],
            token_type=data["token_type"],
            scope=data.get("scope"),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id_token": self.id_token,
            "access_token": self.access_token,
            "refresh_token": self.refresh_token,
            "expires_in": self.expires_in,
            "token_type": self.token_type,
            "scope": self.scope,
        }


@dataclass
class UserProfile:
    user_id: str
    email: str
    email_verified: bool
    name: Optional[str]
    given_name: Optional[str]
    family_name: Optional[str]
    nickname: Optional[str]
    picture: Optional[str]
    locale: Optional[str]
    updated_at: Optional[str]
    provider: str
    custom_claims: Optional[Dict[str, Any]] = None

    @classmethod
    def from_raw_claims(
        cls, raw_claims: Dict[str, Any], provider: str = "auth0"
    ) -> "UserProfile":
        return cls(
            user_id=raw_claims.get("sub", ""),
            email=raw_claims.get("email", ""),
            email_verified=raw_claims.get("email_verified", False),
            name=raw_claims.get("name"),
            given_name=raw_claims.get("given_name"),
            family_name=raw_claims.get("family_name"),
            nickname=raw_claims.get("nickname"),
            picture=raw_claims.get("picture"),
            locale=raw_claims.get("locale", "en"),
            updated_at=raw_claims.get("updated_at"),
            provider=provider,
            custom_claims={
                k: v
                for k, v in raw_claims.items()
                if k
                not in [
                    "sub",
                    "email",
                    "email_verified",
                    "name",
                    "given_name",
                    "family_name",
                    "nickname",
                    "picture",
                    "locale",
                    "updated_at",
                ]
            },
        )

    def to_dict(self) -> Dict[str, Any]:
        result = {
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
        }

        if self.custom_claims:
            result["custom_claims"] = self.custom_claims

        return result

    def get_display_name(self) -> str:
        if self.name:
            return self.name
        if self.given_name and self.family_name:
            return f"{self.given_name} {self.family_name}"
        if self.nickname:
            return self.nickname
        return self.email.split("@")[0]


@dataclass
class AuthRequest:
    state: str
    nonce: str
    redirect_uri: str
    scopes: List[str]
    use_pkce: bool = False
    code_verifier: Optional[str] = None
    code_challenge: Optional[str] = None
    created_at: datetime = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "state": self.state,
            "nonce": self.nonce,
            "redirect_uri": self.redirect_uri,
            "scopes": self.scopes,
            "use_pkce": self.use_pkce,
            "code_verifier": self.code_verifier,
            "code_challenge": self.code_challenge,
            "created_at": self.created_at.isoformat(),
        }


@dataclass
class AuthError:
    error: str
    error_description: Optional[str] = None
    error_uri: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AuthError":
        return cls(
            error=data.get("error", "unknown_error"),
            error_description=data.get("error_description"),
            error_uri=data.get("error_uri"),
        )

    def to_dict(self) -> Dict[str, Any]:
        result = {"error": self.error}
        if self.error_description:
            result["error_description"] = self.error_description
        if self.error_uri:
            result["error_uri"] = self.error_uri
        return result


def normalize_claims(raw_claims: Dict[str, Any], provider: str) -> UserProfile:
    return UserProfile.from_raw_claims(raw_claims, provider)


def validate_token_response(data: Dict[str, Any]) -> bool:
    required_fields = ["access_token", "expires_in", "token_type"]
    return all(field in data for field in required_fields)


def parse_id_token(id_token: str) -> Dict[str, Any]:
    import jwt

    try:
        decoded = jwt.decode(id_token, options={"verify_signature": False})
        return decoded
    except jwt.DecodeError as e:
        raise ValueError(f"Failed to parse ID token: {e}")
