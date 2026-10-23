from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List
from datetime import datetime
import json


@dataclass
class OAuthRequest:
    provider: str
    state: str
    code_verifier: Optional[str] = None
    redirect_uri: Optional[str] = None
    scopes: List[str] = field(default_factory=list)
    extra_params: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "provider": self.provider,
            "state": self.state,
            "code_verifier": self.code_verifier,
            "redirect_uri": self.redirect_uri,
            "scopes": self.scopes,
            "extra_params": self.extra_params,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "OAuthRequest":
        return cls(
            provider=data.get("provider", ""),
            state=data.get("state", ""),
            code_verifier=data.get("code_verifier"),
            redirect_uri=data.get("redirect_uri"),
            scopes=data.get("scopes", []),
            extra_params=data.get("extra_params", {}),
        )


@dataclass
class TokenResponse:
    access_token: str
    token_type: str
    expires_in: Optional[int] = None
    refresh_token: Optional[str] = None
    id_token: Optional[str] = None
    scope: Optional[str] = None
    provider: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "access_token": self.access_token,
            "token_type": self.token_type,
            "expires_in": self.expires_in,
            "refresh_token": self.refresh_token,
            "id_token": self.id_token,
            "scope": self.scope,
            "provider": self.provider,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TokenResponse":
        return cls(
            access_token=data.get("access_token", ""),
            token_type=data.get("token_type", "bearer"),
            expires_in=data.get("expires_in"),
            refresh_token=data.get("refresh_token"),
            id_token=data.get("id_token"),
            scope=data.get("scope"),
            provider=data.get("provider", ""),
        )


@dataclass
class UserProfile:
    id: str
    email: str
    email_verified: bool = False
    name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    picture: Optional[str] = None
    locale: Optional[str] = None
    provider: str = ""
    raw_profile: Dict[str, Any] = field(default_factory=dict)
    additional_claims: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "email": self.email,
            "email_verified": self.email_verified,
            "name": self.name,
            "given_name": self.given_name,
            "family_name": self.family_name,
            "picture": self.picture,
            "locale": self.locale,
            "provider": self.provider,
            "additional_claims": self.additional_claims,
        }

    @classmethod
    def from_raw_profile(
        cls, raw_profile: Dict[str, Any], provider: str
    ) -> "UserProfile":
        if provider == "google":
            return cls(
                id=raw_profile.get("sub", ""),
                email=raw_profile.get("email", ""),
                email_verified=raw_profile.get("email_verified", False),
                name=raw_profile.get("name"),
                given_name=raw_profile.get("given_name"),
                family_name=raw_profile.get("family_name"),
                picture=raw_profile.get("picture"),
                locale=raw_profile.get("locale"),
                provider=provider,
                raw_profile=raw_profile,
            )
        elif provider == "github":
            return cls(
                id=str(raw_profile.get("id", "")),
                email=raw_profile.get("email", ""),
                email_verified=True,
                name=raw_profile.get("name"),
                picture=raw_profile.get("avatar_url"),
                provider=provider,
                raw_profile=raw_profile,
                additional_claims={
                    "login": raw_profile.get("login"),
                    "company": raw_profile.get("company"),
                    "blog": raw_profile.get("blog"),
                    "location": raw_profile.get("location"),
                    "bio": raw_profile.get("bio"),
                },
            )
        elif provider == "auth0":
            return cls(
                id=raw_profile.get("sub", ""),
                email=raw_profile.get("email", ""),
                email_verified=raw_profile.get("email_verified", False),
                name=raw_profile.get("name"),
                picture=raw_profile.get("picture"),
                provider=provider,
                raw_profile=raw_profile,
                additional_claims={"nickname": raw_profile.get("nickname")},
            )
        else:
            return cls(
                id=raw_profile.get("sub", raw_profile.get("id", "")),
                email=raw_profile.get("email", ""),
                email_verified=raw_profile.get("email_verified", False),
                name=raw_profile.get("name"),
                provider=provider,
                raw_profile=raw_profile,
            )


@dataclass
class LoginAuditRecord:
    user_id: str
    provider: str
    timestamp: datetime = field(default_factory=datetime.utcnow)
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    success: bool = True
    error_message: Optional[str] = None
    scopes_used: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "provider": self.provider,
            "timestamp": self.timestamp.isoformat(),
            "ip_address": self.ip_address,
            "user_agent": self.user_agent,
            "success": self.success,
            "error_message": self.error_message,
            "scopes_used": self.scopes_used,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LoginAuditRecord":
        timestamp_str = data.get("timestamp")
        timestamp = (
            datetime.fromisoformat(timestamp_str)
            if timestamp_str
            else datetime.utcnow()
        )

        return cls(
            user_id=data.get("user_id", ""),
            provider=data.get("provider", ""),
            timestamp=timestamp,
            ip_address=data.get("ip_address"),
            user_agent=data.get("user_agent"),
            success=data.get("success", True),
            error_message=data.get("error_message"),
            scopes_used=data.get("scopes_used", []),
        )
