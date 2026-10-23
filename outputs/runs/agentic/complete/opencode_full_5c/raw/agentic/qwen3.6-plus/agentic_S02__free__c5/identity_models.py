import os
import time
import uuid
import base64
import hashlib
import secrets
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from typing import Optional


class AuthProvider(str, Enum):
    AUTH0 = "auth0"
    OKTA = "okta"
    GOOGLE = "google"


class AuditEventType(str, Enum):
    LOGIN_INITIATED = "login_initiated"
    LOGIN_SUCCESS = "login_success"
    LOGIN_FAILURE = "login_failure"
    TOKEN_EXCHANGE = "token_exchange"
    PROFILE_FETCHED = "profile_fetched"
    CONSENT_GRANTED = "consent_granted"
    CONSENT_DENIED = "consent_denied"
    PKCE_FLOW_STARTED = "pkce_flow_started"
    PKCE_FLOW_COMPLETED = "pkce_flow_completed"
    CLAIMS_MODERATED = "claims_moderated"
    CONSENT_TRANSLATED = "consent_translated"


@dataclass
class AuthRequest:
    client_id: str
    redirect_uri: str
    response_type: str = "code"
    scope: str = "openid profile email"
    state: str = field(default_factory=lambda: secrets.token_urlsafe(32))
    nonce: str = field(default_factory=lambda: secrets.token_urlsafe(16))
    connection: Optional[str] = None
    audience: Optional[str] = None
    prompt: Optional[str] = None
    max_age: Optional[int] = None
    acr_values: Optional[str] = None

    def to_query_params(self) -> dict:
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": self.response_type,
            "scope": self.scope,
            "state": self.state,
            "nonce": self.nonce,
        }
        if self.connection:
            params["connection"] = self.connection
        if self.audience:
            params["audience"] = self.audience
        if self.prompt:
            params["prompt"] = self.prompt
        if self.max_age is not None:
            params["max_age"] = str(self.max_age)
        if self.acr_values:
            params["acr_values"] = self.acr_values
        return params


@dataclass
class PKCEState:
    code_verifier: str = field(default_factory=lambda: secrets.token_urlsafe(64))
    state: str = field(default_factory=lambda: secrets.token_urlsafe(32))
    nonce: str = field(default_factory=lambda: secrets.token_urlsafe(16))
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def code_challenge(self) -> str:
        digest = hashlib.sha256(self.code_verifier.encode("ascii")).digest()
        return base64.urlsafe_b64encode(digest).decode("ascii").rstrip("=")

    def to_dict(self) -> dict:
        return {
            "code_verifier": self.code_verifier,
            "state": self.state,
            "nonce": self.nonce,
            "created_at": self.created_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "PKCEState":
        return cls(
            code_verifier=data["code_verifier"],
            state=data["state"],
            nonce=data["nonce"],
            created_at=datetime.fromisoformat(data["created_at"]),
        )


@dataclass
class TokenResponse:
    access_token: str
    token_type: str
    expires_in: int
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    scope: Optional[str] = None
    raw_response: Optional[dict] = None

    @classmethod
    def from_dict(cls, data: dict) -> "TokenResponse":
        return cls(
            access_token=data.get("access_token", ""),
            token_type=data.get("token_type", "Bearer"),
            expires_in=int(data.get("expires_in", 3600)),
            id_token=data.get("id_token"),
            refresh_token=data.get("refresh_token"),
            scope=data.get("scope"),
            raw_response=data,
        )

    @property
    def expires_at(self) -> datetime:
        return datetime.now(timezone.utc).replace(microsecond=0) + __import__(
            "datetime"
        ).timedelta(seconds=self.expires_in)


@dataclass
class NormalizedProfile:
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
    provider: str = "unknown"
    provider_id: Optional[str] = None
    raw_claims: Optional[dict] = None

    @classmethod
    def from_auth0_claims(cls, claims: dict) -> "NormalizedProfile":
        return cls(
            sub=claims.get("sub", ""),
            email=claims.get("email"),
            email_verified=claims.get("email_verified", False),
            name=claims.get("name"),
            given_name=claims.get("given_name"),
            family_name=claims.get("family_name"),
            picture=claims.get("picture"),
            locale=claims.get("locale"),
            phone_number=claims.get("phone_number"),
            phone_number_verified=claims.get("phone_number_verified", False),
            provider="auth0",
            provider_id=claims.get("sub", "").split("|")[-1]
            if "|" in claims.get("sub", "")
            else claims.get("sub"),
            raw_claims=claims,
        )


@dataclass
class AuditRecord:
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    event_type: AuditEventType = AuditEventType.LOGIN_INITIATED
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    provider: str = "auth0"
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    details: Optional[dict] = None
    success: bool = True
    error_message: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "event_id": self.event_id,
            "event_type": self.event_type.value,
            "timestamp": self.timestamp.isoformat(),
            "user_id": self.user_id,
            "session_id": self.session_id,
            "provider": self.provider,
            "ip_address": self.ip_address,
            "user_agent": self.user_agent,
            "details": self.details or {},
            "success": self.success,
            "error_message": self.error_message,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "AuditRecord":
        return cls(
            event_id=data.get("event_id", str(uuid.uuid4())),
            event_type=AuditEventType(data.get("event_type", "login_initiated")),
            timestamp=datetime.fromisoformat(data["timestamp"])
            if "timestamp" in data
            else datetime.now(timezone.utc),
            user_id=data.get("user_id"),
            session_id=data.get("session_id"),
            provider=data.get("provider", "auth0"),
            ip_address=data.get("ip_address"),
            user_agent=data.get("user_agent"),
            details=data.get("details"),
            success=data.get("success", True),
            error_message=data.get("error_message"),
        )


@dataclass
class ModerationResult:
    text: str
    flagged: bool
    categories: dict
    category_scores: dict
    model_used: str = "text-moderation-latest"
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> dict:
        return {
            "text": self.text[:100] + "..." if len(self.text) > 100 else self.text,
            "flagged": self.flagged,
            "categories": self.categories,
            "category_scores": self.category_scores,
            "model_used": self.model_used,
            "timestamp": self.timestamp.isoformat(),
        }


@dataclass
class TranslationResult:
    source_text: str
    translated_text: str
    source_language: str
    target_language: str
    provider: str = "deepl"
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> dict:
        return {
            "source_text": self.source_text,
            "translated_text": self.translated_text,
            "source_language": self.source_language,
            "target_language": self.target_language,
            "provider": self.provider,
            "timestamp": self.timestamp.isoformat(),
        }
