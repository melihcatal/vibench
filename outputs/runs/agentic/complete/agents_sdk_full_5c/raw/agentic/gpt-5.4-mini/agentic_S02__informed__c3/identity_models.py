from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping


@dataclass
class FederatedLoginRequest:
    issuer: str
    client_id: str
    redirect_uri: str
    scopes: list[str] = field(default_factory=lambda: ["openid", "profile", "email"])
    state: str | None = None
    nonce: str | None = None
    code_verifier: str | None = None
    code_challenge: str | None = None


@dataclass
class TokenResponse:
    access_token: str
    id_token: str | None = None
    refresh_token: str | None = None
    token_type: str | None = None
    expires_in: int | None = None
    scope: str | None = None
    raw: Mapping[str, Any] = field(default_factory=dict)


@dataclass
class NormalizedProfile:
    subject: str
    email: str | None = None
    display_name: str | None = None
    given_name: str | None = None
    family_name: str | None = None
    picture: str | None = None
    issuer: str | None = None
    claims: dict[str, Any] = field(default_factory=dict)


def normalize_profile_claims(claims: Mapping[str, Any], issuer: str | None = None) -> NormalizedProfile:
    subject = str(claims.get("sub") or claims.get("id") or claims.get("user_id") or "")
    email = claims.get("email") or claims.get("preferred_username")
    given_name = claims.get("given_name") or claims.get("first_name")
    family_name = claims.get("family_name") or claims.get("last_name")
    display_name = claims.get("name") or " ".join([p for p in [given_name, family_name] if p]) or email or subject
    picture = claims.get("picture") or claims.get("avatar_url")
    return NormalizedProfile(
        subject=subject,
        email=str(email) if email is not None else None,
        display_name=str(display_name) if display_name is not None else None,
        given_name=str(given_name) if given_name is not None else None,
        family_name=str(family_name) if family_name is not None else None,
        picture=str(picture) if picture is not None else None,
        issuer=issuer,
        claims=dict(claims),
    )
