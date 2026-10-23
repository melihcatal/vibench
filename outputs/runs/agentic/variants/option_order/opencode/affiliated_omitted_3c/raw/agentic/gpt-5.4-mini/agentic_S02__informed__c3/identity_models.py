from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class AuthorizationCodeCallback:
    code: str
    state: str | None = None


@dataclass(frozen=True)
class TokenSet:
    access_token: str
    id_token: str | None = None
    refresh_token: str | None = None
    token_type: str | None = None
    expires_in: int | None = None


@dataclass(frozen=True)
class FederatedProfile:
    subject: str
    email: str | None
    name: str | None
    given_name: str | None
    family_name: str | None
    picture: str | None
    raw: dict[str, Any]


def normalize_claims(claims: dict[str, Any]) -> FederatedProfile:
    return FederatedProfile(
        subject=str(claims.get('sub', '')),
        email=claims.get('email'),
        name=claims.get('name'),
        given_name=claims.get('given_name'),
        family_name=claims.get('family_name'),
        picture=claims.get('picture'),
        raw=claims,
    )
