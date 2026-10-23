from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class AuthorizationRequest:
    authorization_url: str
    state: str
    redirect_uri: str
    scope: str


@dataclass(frozen=True)
class TokenResponse:
    access_token: str | None
    id_token: str | None
    refresh_token: str | None
    token_type: str | None
    expires_in: int | None
    raw: dict[str, Any]


@dataclass(frozen=True)
class ProfileClaims:
    subject: str | None
    email: str | None
    email_verified: bool
    display_name: str | None
    given_name: str | None
    family_name: str | None
    picture: str | None
    raw: dict[str, Any]


def normalize_token_response(payload: dict[str, Any]) -> TokenResponse:
    return TokenResponse(
        access_token=payload.get("access_token"),
        id_token=payload.get("id_token"),
        refresh_token=payload.get("refresh_token"),
        token_type=payload.get("token_type"),
        expires_in=payload.get("expires_in"),
        raw=payload,
    )


def normalize_profile_claims(payload: dict[str, Any]) -> ProfileClaims:
    return ProfileClaims(
        subject=payload.get("sub"),
        email=payload.get("email"),
        email_verified=bool(payload.get("email_verified", False)),
        display_name=payload.get("name") or payload.get("nickname"),
        given_name=payload.get("given_name"),
        family_name=payload.get("family_name"),
        picture=payload.get("picture"),
        raw=payload,
    )
