import os
import secrets
import hashlib
import base64
import time
import uuid
from dataclasses import dataclass, field, asdict
from typing import Optional, Dict, List, Any
from enum import Enum


class GrantType(str, Enum):
    AUTHORIZATION_CODE = "authorization_code"
    PKCE = "pkce"


class AuditEventType(str, Enum):
    LOGIN_INITIATED = "login_initiated"
    LOGIN_COMPLETED = "login_completed"
    LOGIN_FAILED = "login_failed"
    TOKEN_EXCHANGED = "token_exchanged"
    PROFILE_FETCHED = "profile_fetched"
    CONSENT_GRANTED = "consent_granted"
    CONSENT_DENIED = "consent_denied"
    SESSION_CREATED = "session_created"
    SESSION_EXPIRED = "session_expired"


@dataclass
class OAuthConfig:
    domain: str = ""
    client_id: str = ""
    client_secret: str = ""
    redirect_uri: str = ""
    audience: str = ""
    scope: str = "openid profile email"
    response_type: str = "code"
    issuer: str = ""

    def __post_init__(self):
        if not self.domain:
            self.domain = os.getenv("AUTH0_DOMAIN", "")
        if not self.client_id:
            self.client_id = os.getenv("AUTH0_CLIENT_ID", "")
        if not self.client_secret:
            self.client_secret = os.getenv("AUTH0_CLIENT_SECRET", "")
        if not self.redirect_uri:
            self.redirect_uri = os.getenv(
                "AUTH0_REDIRECT_URI", "http://localhost:3000/callback"
            )
        if not self.audience:
            self.audience = os.getenv("AUTH0_AUDIENCE", "")
        if not self.issuer:
            self.issuer = f"https://{self.domain}" if self.domain else ""

    @property
    def authorize_url(self) -> str:
        return f"https://{self.domain}/authorize"

    @property
    def token_url(self) -> str:
        return f"https://{self.domain}/oauth/token"

    @property
    def userinfo_url(self) -> str:
        return f"https://{self.domain}/userinfo"


@dataclass
class AuthorizationRequest:
    client_id: str
    redirect_uri: str
    response_type: str = "code"
    scope: str = "openid profile email"
    state: str = ""
    nonce: str = ""
    audience: str = ""
    code_challenge: str = ""
    code_challenge_method: str = ""
    connection: str = ""

    def __post_init__(self):
        if not self.state:
            self.state = secrets.token_urlsafe(32)
        if not self.nonce:
            self.nonce = secrets.token_urlsafe(32)

    def to_query_params(self) -> Dict[str, str]:
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": self.response_type,
            "scope": self.scope,
            "state": self.state,
            "nonce": self.nonce,
        }
        if self.audience:
            params["audience"] = self.audience
        if self.code_challenge:
            params["code_challenge"] = self.code_challenge
        if self.code_challenge_method:
            params["code_challenge_method"] = self.code_challenge_method
        if self.connection:
            params["connection"] = self.connection
        return params


@dataclass
class TokenResponse:
    access_token: str = ""
    id_token: str = ""
    refresh_token: str = ""
    token_type: str = "Bearer"
    expires_in: int = 0
    scope: str = ""

    @property
    def is_valid(self) -> bool:
        return bool(self.access_token) and self.expires_in > 0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class UserProfile:
    sub: str = ""
    name: str = ""
    email: str = ""
    email_verified: bool = False
    picture: str = ""
    nickname: str = ""
    given_name: str = ""
    family_name: str = ""
    locale: str = ""
    zoneinfo: str = ""
    updated_at: int = 0
    identities: List[Dict[str, Any]] = field(default_factory=list)
    raw_claims: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class NormalizedClaims:
    user_id: str = ""
    email: str = ""
    email_verified: bool = False
    display_name: str = ""
    first_name: str = ""
    last_name: str = ""
    avatar_url: str = ""
    locale: str = ""
    provider: str = ""
    provider_user_id: str = ""
    federated_at: str = ""
    extra_attributes: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class PkcePair:
    code_verifier: str = ""
    code_challenge: str = ""
    code_challenge_method: str = "S256"

    @staticmethod
    def generate() -> "PkcePair":
        code_verifier = secrets.token_urlsafe(64)
        digest = hashlib.sha256(code_verifier.encode("ascii")).digest()
        code_challenge = base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")
        return PkcePair(
            code_verifier=code_verifier,
            code_challenge=code_challenge,
            code_challenge_method="S256",
        )


@dataclass
class AuditEvent:
    event_id: str = ""
    event_type: str = ""
    timestamp: str = ""
    user_id: str = ""
    session_id: str = ""
    ip_address: str = ""
    user_agent: str = ""
    provider: str = ""
    connection: str = ""
    details: Dict[str, Any] = field(default_factory=dict)
    risk_score: float = 0.0
    status: str = "success"

    def __post_init__(self):
        if not self.event_id:
            self.event_id = str(uuid.uuid4())
        if not self.timestamp:
            self.timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        if not self.session_id:
            self.session_id = secrets.token_urlsafe(16)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class AuditSummary:
    total_events: int = 0
    successful_logins: int = 0
    failed_logins: int = 0
    unique_users: int = 0
    unique_providers: int = 0
    time_range_start: str = ""
    time_range_end: str = ""
    summary_text: str = ""
    risk_flags: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ModerationResult:
    text: str = ""
    is_safe: bool = True
    categories: Dict[str, float] = field(default_factory=dict)
    overall_score: float = 0.0
    flagged: bool = False
    details: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class TranslationResult:
    source_text: str = ""
    translated_text: str = ""
    source_language: str = ""
    target_language: str = ""
    confidence: float = 1.0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
