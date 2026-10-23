import os
import time
import uuid
import secrets
import hashlib
import base64
from dataclasses import dataclass, field, asdict
from typing import Optional, Dict, List, Any
from enum import Enum


class AuthFlowType(Enum):
    AUTHORIZATION_CODE = "authorization_code"
    PKCE = "pkce"
    IMPLICIT = "implicit"


class AuditEventType(Enum):
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
    provider: str
    client_id: str
    client_secret: str
    redirect_uri: str
    authorization_endpoint: str
    token_endpoint: str
    userinfo_endpoint: str
    scope: str = "openid profile email"
    response_type: str = "code"
    state: str = ""
    nonce: str = ""
    audience: Optional[str] = None
    connection: Optional[str] = None

    def __post_init__(self):
        if not self.state:
            self.state = secrets.token_urlsafe(32)
        if not self.nonce:
            self.nonce = secrets.token_urlsafe(32)


@dataclass
class PKCEConfig:
    code_verifier: str = ""
    code_challenge: str = ""
    code_challenge_method: str = "S256"

    def generate(self):
        self.code_verifier = secrets.token_urlsafe(64)
        code_verifier_bytes = self.code_verifier.encode("ascii")
        sha256_hash = hashlib.sha256(code_verifier_bytes).digest()
        self.code_challenge = (
            base64.urlsafe_b64encode(sha256_hash).rstrip(b"=").decode("ascii")
        )
        return self


@dataclass
class TokenResponse:
    access_token: str
    token_type: str = "Bearer"
    expires_in: int = 3600
    refresh_token: Optional[str] = None
    id_token: Optional[str] = None
    scope: Optional[str] = None
    issued_at: float = field(default_factory=time.time)

    def is_expired(self) -> bool:
        return time.time() >= (self.issued_at + self.expires_in)


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
    phone_number_verified: bool = False
    address: Optional[Dict[str, str]] = None
    updated_at: Optional[float] = None
    raw_claims: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class AuditEvent:
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    event_type: str = AuditEventType.LOGIN_INITIATED.value
    timestamp: float = field(default_factory=time.time)
    user_sub: Optional[str] = None
    session_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    provider: str = ""
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    status: str = "success"
    details: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class AuditSummary:
    total_events: int = 0
    events_by_type: Dict[str, int] = field(default_factory=dict)
    events_by_status: Dict[str, int] = field(default_factory=dict)
    events_by_provider: Dict[str, int] = field(default_factory=dict)
    unique_users: int = 0
    time_range: Dict[str, float] = field(default_factory=dict)
    raw_events: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class ClaimsModerationRequest:
    text: str
    user_sub: Optional[str] = None
    context: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ClaimsModerationResult:
    flagged: bool = False
    categories: Dict[str, float] = field(default_factory=dict)
    category_applied_action: Dict[str, str] = field(default_factory=dict)
    explanation: Optional[str] = None
    confidence: float = 0.0
    raw_response: Optional[Dict[str, Any]] = None


@dataclass
class ConsentTranslationRequest:
    text: str
    source_language: str = "en"
    target_language: str = "es"
    context: Optional[str] = None


@dataclass
class ConsentTranslationResult:
    translated_text: str
    source_language: str
    target_language: str
    detected_language: Optional[str] = None
    confidence: float = 0.0
    raw_response: Optional[Dict[str, Any]] = None


@dataclass
class AuthorizationRequest:
    client_id: str
    redirect_uri: str
    scope: str
    response_type: str = "code"
    state: str = ""
    nonce: str = ""
    code_challenge: Optional[str] = None
    code_challenge_method: Optional[str] = None
    audience: Optional[str] = None
    connection: Optional[str] = None
    prompt: Optional[str] = None
    max_age: Optional[int] = None
    ui_locales: Optional[str] = None
    acr_values: Optional[str] = None

    def to_params(self) -> Dict[str, str]:
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": self.scope,
            "response_type": self.response_type,
            "state": self.state,
            "nonce": self.nonce,
        }
        if self.code_challenge:
            params["code_challenge"] = self.code_challenge
        if self.code_challenge_method:
            params["code_challenge_method"] = self.code_challenge_method
        if self.audience:
            params["audience"] = self.audience
        if self.connection:
            params["connection"] = self.connection
        if self.prompt:
            params["prompt"] = self.prompt
        if self.max_age is not None:
            params["max_age"] = str(self.max_age)
        if self.ui_locales:
            params["ui_locales"] = self.ui_locales
        if self.acr_values:
            params["acr_values"] = self.acr_values
        return params


@dataclass
class TokenExchangeRequest:
    grant_type: str = "authorization_code"
    code: str = ""
    redirect_uri: str = ""
    client_id: str = ""
    client_secret: str = ""
    code_verifier: Optional[str] = None

    def to_form_data(self) -> Dict[str, str]:
        data = {
            "grant_type": self.grant_type,
            "code": self.code,
            "redirect_uri": self.redirect_uri,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        if self.code_verifier:
            data["code_verifier"] = self.code_verifier
        return data


def normalize_claims(raw_claims: Dict[str, Any]) -> UserProfile:
    profile = UserProfile(
        sub=raw_claims.get("sub", ""),
        email=raw_claims.get("email"),
        email_verified=raw_claims.get("email_verified", False),
        name=raw_claims.get("name"),
        given_name=raw_claims.get("given_name"),
        family_name=raw_claims.get("family_name"),
        picture=raw_claims.get("picture"),
        locale=raw_claims.get("locale"),
        phone_number=raw_claims.get("phone_number"),
        phone_number_verified=raw_claims.get("phone_number_verified", False),
        address=raw_claims.get("address"),
        updated_at=raw_claims.get("updated_at"),
        raw_claims=raw_claims,
    )
    return profile


def build_audit_event(
    event_type: AuditEventType,
    user_sub: Optional[str] = None,
    provider: str = "",
    status: str = "success",
    details: Optional[Dict[str, Any]] = None,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
) -> AuditEvent:
    return AuditEvent(
        event_type=event_type.value,
        user_sub=user_sub,
        provider=provider,
        status=status,
        details=details or {},
        ip_address=ip_address,
        user_agent=user_agent,
    )
