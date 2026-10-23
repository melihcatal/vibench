"""
Local request, response, and normalization helpers for Federated Login Flow.

Defines dataclasses for OAuth requests, token responses, federated user claims,
and claim normalization utilities.
"""

import re
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum


class AuthFlowType(str, Enum):
    """OAuth/OIDC authorization flow types."""
    AUTHORIZATION_CODE = "authorization_code"
    PKCE = "pkce"
    IMPLICIT = "implicit"
    CLIENT_CREDENTIALS = "client_credentials"


class TokenType(str, Enum):
    """Token types returned by identity providers."""
    BEARER = "Bearer"
    MAC = "MAC"
    DPoP = "DPoP"


@dataclass
class AuthorizationRequest:
    """OAuth authorization request parameters."""
    client_id: str
    redirect_uri: str
    response_type: str = "code"
    scope: str = "openid profile email"
    state: str = ""
    nonce: str = ""
    code_challenge: Optional[str] = None
    code_challenge_method: Optional[str] = "S256"
    audience: Optional[str] = None
    prompt: Optional[str] = None
    max_age: Optional[int] = None
    extra_params: Dict[str, str] = field(default_factory=dict)


@dataclass
class TokenResponse:
    """OAuth token endpoint response."""
    access_token: str
    token_type: TokenType = TokenType.BEARER
    expires_in: int = 3600
    refresh_token: Optional[str] = None
    id_token: Optional[str] = None
    scope: Optional[str] = None
    provider: str = ""


@dataclass
class FederatedUserClaims:
    """Normalized federated user profile claims."""
    provider: str
    provider_user_id: str
    email: str
    email_verified: bool = False
    given_name: str = ""
    family_name: str = ""
    full_name: str = ""
    preferred_username: str = ""
    locale: str = ""
    timezone: str = ""
    picture_url: str = ""
    phone_number: str = ""
    phone_verified: bool = False
    raw_claims: Dict[str, Any] = field(default_factory=dict)
    custom_attributes: Dict[str, Any] = field(default_factory=dict)
    fetched_at: int = 0


@dataclass
class ClaimNormalizationResult:
    """Result of claim normalization operation."""
    success: bool
    claims: Optional[FederatedUserClaims] = None
    error: Optional[str] = None
    provider: str = ""
    fetched_at: int = 0


@dataclass
class LoginAuditEvent:
    """Federated login audit event record."""
    event_id: str
    session_id: str
    provider: str
    user_id: str
    email: str
    action: str  # login_start, login_success, login_failure, logout
    timestamp: int
    ip_address: str = ""
    user_agent: str = ""
    auth_flow: str = ""
    error_message: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ConsentRecord:
    """User consent record for identity provider."""
    user_id: str
    provider: str
    scope: str
    consented_at: int
    consent_text: str = ""
    translated_text: str = ""
    language: str = "en"


# Email normalization patterns
EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")


def normalize_email(email: str) -> str:
    """Normalize email address: lowercase and strip whitespace."""
    if not email:
        return ""
    email = email.strip().lower()
    if not EMAIL_REGEX.match(email):
        return ""
    return email


def normalize_name(given_name: str = "", family_name: str = "", fallback: str = "") -> str:
    """Normalize user name from given/family name components."""
    given = given_name.strip() if given_name else ""
    family = family_name.strip() if family_name else ""

    if given or family:
        return f"{given} {family}".strip()

    return fallback.strip() if fallback else ""


def normalize_claims(raw_claims: Dict[str, Any], provider: str = "") -> Dict[str, Any]:
    """
    Normalize raw claims from any provider to standard format.

    Handles provider-specific claim naming conventions.
    """
    normalized = {}

    # Standard OIDC claims
    normalized["sub"] = raw_claims.get("sub", "")
    normalized["email"] = normalize_email(raw_claims.get("email", ""))
    normalized["email_verified"] = bool(raw_claims.get("email_verified", False))
    normalized["given_name"] = raw_claims.get("given_name", "")
    normalized["family_name"] = raw_claims.get("family_name", "")
    normalized["name"] = normalize_name(
        normalized["given_name"],
        normalized["family_name"],
        raw_claims.get("name", ""),
    )
    normalized["preferred_username"] = raw_claims.get("preferred_username", normalized["email"])
    normalized["picture"] = raw_claims.get("picture", "")
    normalized["locale"] = raw_claims.get("locale", "")
    normalized["zoneinfo"] = raw_claims.get("zoneinfo", "")

    # Provider-specific mappings
    if provider == "google":
        normalized["given_name"] = raw_claims.get("given_name", "")
        normalized["family_name"] = raw_claims.get("family_name", "")
    elif provider == "azure_ad":
        normalized["given_name"] = raw_claims.get("given_name", raw_claims.get("name", ""))
        normalized["family_name"] = raw_claims.get("family_name", "")

    return normalized


def create_audit_event(
    event_id: str,
    session_id: str,
    provider: str,
    action: str,
    timestamp: int = 0,
    **kwargs,
) -> LoginAuditEvent:
    """Create a standardized login audit event."""
    if not timestamp:
        import time
        timestamp = int(time.time())

    return LoginAuditEvent(
        event_id=event_id,
        session_id=session_id,
        provider=provider,
        user_id=kwargs.get("user_id", ""),
        email=kwargs.get("email", ""),
        action=action,
        timestamp=timestamp,
        ip_address=kwargs.get("ip_address", ""),
        user_agent=kwargs.get("user_agent", ""),
        auth_flow=kwargs.get("auth_flow", ""),
        error_message=kwargs.get("error_message", ""),
        metadata=kwargs.get("metadata", {}),
    )
