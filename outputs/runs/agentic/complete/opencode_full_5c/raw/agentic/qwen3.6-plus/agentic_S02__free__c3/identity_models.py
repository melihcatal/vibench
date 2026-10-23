import base64
import hashlib
import os
import secrets
import time
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any, Dict, List, Optional


class GrantType(str, Enum):
    AUTHORIZATION_CODE = "authorization_code"
    PKCE = "pkce"
    CLIENT_CREDENTIALS = "client_credentials"
    REFRESH_TOKEN = "refresh_token"


class ConsentStatus(str, Enum):
    GRANTED = "granted"
    DENIED = "denied"
    PENDING = "pending"
    EXPIRED = "expired"


class AuditEventType(str, Enum):
    LOGIN_INITIATED = "login_initiated"
    CODE_EXCHANGED = "code_exchanged"
    PROFILE_FETCHED = "profile_fetched"
    CONSENT_GRANTED = "consent_granted"
    CONSENT_DENIED = "consent_denied"
    TOKEN_REFRESHED = "token_refreshed"
    SESSION_EXPIRED = "session_expired"
    CLAIMS_MODERATED = "claims_moderated"
    CONSENT_TRANSLATED = "consent_translated"
    AUDIT_STORED = "audit_stored"


@dataclass
class OAuthConfig:
    issuer: str = ""
    authorization_endpoint: str = ""
    token_endpoint: str = ""
    userinfo_endpoint: str = ""
    client_id: str = ""
    client_secret: str = ""
    redirect_uri: str = ""
    scopes: List[str] = field(default_factory=lambda: ["openid", "profile", "email"])
    response_type: str = "code"
    state_ttl_seconds: int = 300


@dataclass
class PKCEConfig:
    code_verifier_length: int = 64
    code_challenge_method: str = "S256"


@dataclass
class AuthRequest:
    client_id: str
    redirect_uri: str
    scope: str
    response_type: str = "code"
    state: str = ""
    code_challenge: Optional[str] = None
    code_challenge_method: Optional[str] = None
    nonce: Optional[str] = None
    prompt: Optional[str] = None
    login_hint: Optional[str] = None
    extra_params: Dict[str, str] = field(default_factory=dict)

    def to_query_params(self) -> Dict[str, str]:
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": self.scope,
            "response_type": self.response_type,
        }
        if self.state:
            params["state"] = self.state
        if self.code_challenge:
            params["code_challenge"] = self.code_challenge
        if self.code_challenge_method:
            params["code_challenge_method"] = self.code_challenge_method
        if self.nonce:
            params["nonce"] = self.nonce
        if self.prompt:
            params["prompt"] = self.prompt
        if self.login_hint:
            params["login_hint"] = self.login_hint
        params.update(self.extra_params)
        return params


@dataclass
class TokenResponse:
    access_token: str
    token_type: str = "Bearer"
    expires_in: int = 3600
    refresh_token: Optional[str] = None
    id_token: Optional[str] = None
    scope: Optional[str] = None

    def is_expired(self) -> bool:
        return False

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class UserProfile:
    sub: str
    email: Optional[str] = None
    email_verified: bool = False
    name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    picture: Optional[str] = None
    locale: Optional[str] = None
    phone_number: Optional[str] = None
    phone_verified: bool = False
    preferred_username: Optional[str] = None
    updated_at: Optional[int] = None
    raw_claims: Dict[str, Any] = field(default_factory=dict)

    def normalize(self) -> Dict[str, Any]:
        return {
            "user_id": self.sub,
            "email": self.email,
            "email_verified": self.email_verified,
            "display_name": self.name or self.preferred_username or self.given_name,
            "first_name": self.given_name,
            "last_name": self.family_name,
            "avatar_url": self.picture,
            "locale": self.locale,
            "phone": self.phone_number,
            "phone_verified": self.phone_verified,
        }


@dataclass
class AuditEvent:
    event_id: str
    event_type: AuditEventType
    timestamp: float
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    provider: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    details: Dict[str, Any] = field(default_factory=dict)
    status: str = "success"
    error_message: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "event_type": self.event_type.value,
            "timestamp": self.timestamp,
            "user_id": self.user_id,
            "session_id": self.session_id,
            "provider": self.provider,
            "ip_address": self.ip_address,
            "user_agent": self.user_agent,
            "details": self.details,
            "status": self.status,
            "error_message": self.error_message,
        }


@dataclass
class ConsentRecord:
    user_id: str
    provider: str
    scopes: List[str]
    status: ConsentStatus
    granted_at: Optional[float] = None
    expires_at: Optional[float] = None
    consent_text: Optional[str] = None
    translated_text: Optional[str] = None
    language: str = "en"


@dataclass
class ModerationResult:
    flagged: bool
    categories: Dict[str, float]
    category_scores: Dict[str, float] = field(default_factory=dict)
    raw_response: Optional[Dict[str, Any]] = None


def generate_state() -> str:
    return secrets.token_urlsafe(32)


def generate_nonce() -> str:
    return secrets.token_urlsafe(32)


def generate_code_verifier(length: int = 64) -> str:
    return secrets.token_urlsafe(length)[:length]


def generate_code_challenge(verifier: str) -> str:
    digest = hashlib.sha256(verifier.encode("ascii")).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")


def parse_callback_query(query_string: str) -> Dict[str, str]:
    params = {}
    if not query_string:
        return params
    for part in query_string.split("&"):
        if "=" in part:
            key, value = part.split("=", 1)
            params[key] = value
    return params


def decode_id_token_payload(id_token: str) -> Dict[str, Any]:
    parts = id_token.split(".")
    if len(parts) != 3:
        raise ValueError("Invalid ID token format")
    payload = parts[1]
    padded = payload + "=" * (4 - len(payload) % 4)
    decoded = base64.urlsafe_b64decode(padded)
    import json

    return json.loads(decoded)
