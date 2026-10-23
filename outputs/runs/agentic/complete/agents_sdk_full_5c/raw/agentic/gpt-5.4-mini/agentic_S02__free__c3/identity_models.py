from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping


@dataclass(frozen=True)
class LoginRequest:
    state: str
    redirect_uri: str | None = None
    scope: str | None = None
    nonce: str | None = None
    prompt: str | None = None
    connection: str | None = None


@dataclass(frozen=True)
class PKCELoginRequest:
    state: str
    redirect_uri: str | None = None
    scope: str | None = None
    prompt: str | None = None


@dataclass(frozen=True)
class OAuthCallbackRequest:
    code: str
    state: str
    redirect_uri: str | None = None
    code_verifier: str | None = None


@dataclass(frozen=True)
class TokenSet:
    access_token: str
    id_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"
    expires_in: int = 0
    raw: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "access_token": self.access_token,
            "id_token": self.id_token,
            "refresh_token": self.refresh_token,
            "token_type": self.token_type,
            "expires_in": self.expires_in,
            "raw": dict(self.raw),
        }


@dataclass(frozen=True)
class NormalizedProfile:
    issuer: str
    subject: str
    email: str | None = None
    display_name: str | None = None
    given_name: str | None = None
    family_name: str | None = None
    locale: str | None = None
    raw: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "issuer": self.issuer,
            "subject": self.subject,
            "email": self.email,
            "display_name": self.display_name,
            "given_name": self.given_name,
            "family_name": self.family_name,
            "locale": self.locale,
            "raw": dict(self.raw),
        }


def normalize_profile_claims(claims: Mapping[str, Any], issuer: str) -> NormalizedProfile:
    subject = str(claims.get("sub", ""))
    display_name = claims.get("name") or claims.get("preferred_username")
    return NormalizedProfile(
        issuer=issuer,
        subject=subject,
        email=claims.get("email"),
        display_name=display_name,
        given_name=claims.get("given_name"),
        family_name=claims.get("family_name"),
        locale=claims.get("locale"),
        raw=claims,
    )
