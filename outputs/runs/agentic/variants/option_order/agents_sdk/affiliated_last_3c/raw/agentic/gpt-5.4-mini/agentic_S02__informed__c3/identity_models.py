from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class LoginRequest:
    issuer: str
    client_id: str
    redirect_uri: str
    scopes: tuple[str, ...] = ("openid", "profile", "email")
    state: Optional[str] = None
    nonce: Optional[str] = None
    code_verifier: Optional[str] = None
    code_challenge: Optional[str] = None


@dataclass(frozen=True)
class TokenResponse:
    access_token: str
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    expires_in: Optional[int] = None
    token_type: str = "Bearer"
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class NormalizedProfile:
    subject: str
    email: Optional[str] = None
    display_name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    issuer: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class AuditEvent:
    event_type: str
    subject: str
    provider: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ModerationResult:
    text: str
    flagged: bool
    score: Optional[float] = None
    labels: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class TranslationResult:
    source_text: str
    translated_text: str
    source_language: Optional[str] = None
    target_language: Optional[str] = None
    provider: str = ""


@dataclass(frozen=True)
class DocumentRecord:
    id: str
    type: str
    data: Dict[str, Any] = field(default_factory=dict)
