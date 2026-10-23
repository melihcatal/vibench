from dataclasses import dataclass, field
from typing import Any, Dict, Mapping, Optional
import hashlib
import json
import re


_WHITESPACE_RE = re.compile(r"\s+")


def _normalize_string(value: Any) -> str:
    if value is None:
        return ""
    text = str(value).strip()
    return _WHITESPACE_RE.sub(" ", text)


def _normalize_dict(data: Optional[Mapping[str, Any]]) -> Dict[str, Any]:
    if not data:
        return {}
    return {str(key): value for key, value in data.items()}


def stable_fingerprint(payload: Mapping[str, Any]) -> str:
    normalized = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class LoginRequest:
    issuer: str
    client_id: str
    redirect_uri: str
    scope: str = "openid profile email"
    state: str = ""
    nonce: str = ""
    code_challenge: str = ""
    code_challenge_method: str = "S256"
    extra_params: Dict[str, Any] = field(default_factory=dict)

    def normalized(self) -> "LoginRequest":
        return LoginRequest(
            issuer=_normalize_string(self.issuer),
            client_id=_normalize_string(self.client_id),
            redirect_uri=_normalize_string(self.redirect_uri),
            scope=_normalize_string(self.scope) or "openid profile email",
            state=_normalize_string(self.state),
            nonce=_normalize_string(self.nonce),
            code_challenge=_normalize_string(self.code_challenge),
            code_challenge_method=_normalize_string(self.code_challenge_method) or "S256",
            extra_params=_normalize_dict(self.extra_params),
        )


@dataclass(frozen=True)
class TokenResponse:
    access_token: str = ""
    id_token: str = ""
    refresh_token: str = ""
    token_type: str = "Bearer"
    expires_in: int = 0
    scope: str = ""
    raw: Dict[str, Any] = field(default_factory=dict)

    def normalized(self) -> "TokenResponse":
        expires_in = self.expires_in
        if isinstance(expires_in, str) and expires_in.isdigit():
            expires_in = int(expires_in)
        return TokenResponse(
            access_token=_normalize_string(self.access_token),
            id_token=_normalize_string(self.id_token),
            refresh_token=_normalize_string(self.refresh_token),
            token_type=_normalize_string(self.token_type) or "Bearer",
            expires_in=int(expires_in) if expires_in else 0,
            scope=_normalize_string(self.scope),
            raw=_normalize_dict(self.raw),
        )


@dataclass(frozen=True)
class UserProfileClaims:
    subject: str = ""
    email: str = ""
    email_verified: bool = False
    name: str = ""
    given_name: str = ""
    family_name: str = ""
    picture: str = ""
    locale: str = ""
    raw: Dict[str, Any] = field(default_factory=dict)

    def normalized(self) -> "UserProfileClaims":
        raw = _normalize_dict(self.raw)
        email_verified = self.email_verified
        if isinstance(email_verified, str):
            email_verified = email_verified.lower() in {"1", "true", "yes", "y"}
        return UserProfileClaims(
            subject=_normalize_string(self.subject),
            email=_normalize_string(self.email).lower(),
            email_verified=bool(email_verified),
            name=_normalize_string(self.name),
            given_name=_normalize_string(self.given_name),
            family_name=_normalize_string(self.family_name),
            picture=_normalize_string(self.picture),
            locale=_normalize_string(self.locale).lower(),
            raw=raw,
        )


def normalize_login_request(data: Mapping[str, Any]) -> LoginRequest:
    return LoginRequest(
        issuer=data.get("issuer", ""),
        client_id=data.get("client_id", ""),
        redirect_uri=data.get("redirect_uri", ""),
        scope=data.get("scope", "openid profile email"),
        state=data.get("state", ""),
        nonce=data.get("nonce", ""),
        code_challenge=data.get("code_challenge", ""),
        code_challenge_method=data.get("code_challenge_method", "S256"),
        extra_params=data.get("extra_params", {}) or {},
    ).normalized()


def normalize_token_response(data: Mapping[str, Any]) -> TokenResponse:
    return TokenResponse(
        access_token=data.get("access_token", ""),
        id_token=data.get("id_token", ""),
        refresh_token=data.get("refresh_token", ""),
        token_type=data.get("token_type", "Bearer"),
        expires_in=data.get("expires_in", 0),
        scope=data.get("scope", ""),
        raw=dict(data),
    ).normalized()


def normalize_user_profile_claims(data: Mapping[str, Any]) -> UserProfileClaims:
    return UserProfileClaims(
        subject=data.get("sub", "") or data.get("subject", ""),
        email=data.get("email", ""),
        email_verified=data.get("email_verified", False),
        name=data.get("name", ""),
        given_name=data.get("given_name", ""),
        family_name=data.get("family_name", ""),
        picture=data.get("picture", ""),
        locale=data.get("locale", ""),
        raw=dict(data),
    ).normalized()


__all__ = [
    "LoginRequest",
    "TokenResponse",
    "UserProfileClaims",
    "normalize_login_request",
    "normalize_token_response",
    "normalize_user_profile_claims",
    "stable_fingerprint",
]
