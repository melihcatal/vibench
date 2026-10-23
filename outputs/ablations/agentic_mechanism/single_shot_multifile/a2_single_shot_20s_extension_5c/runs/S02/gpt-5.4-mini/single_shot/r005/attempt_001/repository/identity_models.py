from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class LoginStartRequest:
    state: str | None = None
    nonce: str | None = None
    prompt: str | None = None
    login_hint: str | None = None
    scope: str | None = None


@dataclass(frozen=True)
class LoginStartResponse:
    authorize_url: str
    state: str
    nonce: str
    provider: str


@dataclass(frozen=True)
class PkceLoginRequest:
    state: str | None = None
    nonce: str | None = None
    code_verifier: str | None = None
    prompt: str | None = None
    login_hint: str | None = None
    scope: str | None = None


@dataclass(frozen=True)
class PkceLoginResponse:
    authorize_url: str
    state: str
    nonce: str
    code_verifier: str
    provider: str


@dataclass(frozen=True)
class CallbackExchangeRequest:
    code: str
    redirect_uri: str
    code_verifier: str | None = None


@dataclass(frozen=True)
class TokenSet:
    access_token: str
    id_token: str
    refresh_token: str | None
    expires_in: int | None
    token_type: str | None
    scope: str | None
    claims: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ProfileClaims:
    subject: str
    email: str
    email_verified: bool
    display_name: str
    given_name: str | None
    family_name: str | None
    picture: str | None
    locale: str | None
    provider: str
    raw: dict[str, Any] = field(default_factory=dict)
