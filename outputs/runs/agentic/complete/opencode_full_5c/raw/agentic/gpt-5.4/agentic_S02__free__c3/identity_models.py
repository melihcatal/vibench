from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def compact_dict(values: Dict[str, Any]) -> Dict[str, Any]:
    return {key: value for key, value in values.items() if value is not None}


@dataclass
class OAuthLoginRequest:
    state: str
    redirect_uri: str
    scopes: List[str] = field(default_factory=list)
    prompt: Optional[str] = None
    login_hint: Optional[str] = None
    nonce: Optional[str] = None

    def to_params(self) -> Dict[str, str]:
        return {
            key: str(value)
            for key, value in compact_dict(
                {
                    "state": self.state,
                    "redirect_uri": self.redirect_uri,
                    "scope": " ".join(self.scopes),
                    "prompt": self.prompt,
                    "login_hint": self.login_hint,
                    "nonce": self.nonce,
                }
            ).items()
        }


@dataclass
class PKCELoginRequest(OAuthLoginRequest):
    code_challenge: str = ""
    code_challenge_method: str = "S256"

    def to_params(self) -> Dict[str, str]:
        params = super().to_params()
        params.update(
            {
                "code_challenge": self.code_challenge,
                "code_challenge_method": self.code_challenge_method,
            }
        )
        return params


@dataclass
class CallbackRequest:
    code: str
    redirect_uri: str
    state: Optional[str] = None
    code_verifier: Optional[str] = None


@dataclass
class TokenSet:
    access_token: str
    token_type: str
    expires_in: Optional[int] = None
    refresh_token: Optional[str] = None
    id_token: Optional[str] = None
    scope: Optional[str] = None
    provider: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_payload(
        cls, payload: Dict[str, Any], provider: Optional[str] = None
    ) -> "TokenSet":
        return cls(
            access_token=payload["access_token"],
            token_type=payload.get("token_type", "Bearer"),
            expires_in=payload.get("expires_in"),
            refresh_token=payload.get("refresh_token"),
            id_token=payload.get("id_token"),
            scope=payload.get("scope"),
            provider=provider,
            raw=payload,
        )

    def to_dict(self) -> Dict[str, Any]:
        return compact_dict(
            {
                "access_token": self.access_token,
                "token_type": self.token_type,
                "expires_in": self.expires_in,
                "refresh_token": self.refresh_token,
                "id_token": self.id_token,
                "scope": self.scope,
                "provider": self.provider,
                "raw": self.raw,
            }
        )


@dataclass
class NormalizedProfile:
    provider: str
    subject: str
    email: Optional[str] = None
    email_verified: Optional[bool] = None
    full_name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    picture: Optional[str] = None
    locale: Optional[str] = None
    updated_at: Optional[str] = None
    raw_claims: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return compact_dict(
            {
                "provider": self.provider,
                "subject": self.subject,
                "email": self.email,
                "email_verified": self.email_verified,
                "full_name": self.full_name,
                "given_name": self.given_name,
                "family_name": self.family_name,
                "picture": self.picture,
                "locale": self.locale,
                "updated_at": self.updated_at,
                "raw_claims": self.raw_claims,
            }
        )


@dataclass
class AuditEvent:
    event_id: str
    occurred_at: str
    provider: str
    event_type: str
    actor_subject: Optional[str] = None
    actor_email: Optional[str] = None
    session_id: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    outcome: Optional[str] = None
    details: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def create(
        cls, event_id: str, provider: str, event_type: str, **kwargs: Any
    ) -> "AuditEvent":
        return cls(
            event_id=event_id,
            occurred_at=kwargs.pop("occurred_at", utc_now_iso()),
            provider=provider,
            event_type=event_type,
            actor_subject=kwargs.pop("actor_subject", None),
            actor_email=kwargs.pop("actor_email", None),
            session_id=kwargs.pop("session_id", None),
            ip_address=kwargs.pop("ip_address", None),
            user_agent=kwargs.pop("user_agent", None),
            outcome=kwargs.pop("outcome", None),
            details=kwargs.pop("details", {}),
        )

    def to_dict(self) -> Dict[str, Any]:
        return compact_dict(
            {
                "event_id": self.event_id,
                "occurred_at": self.occurred_at,
                "provider": self.provider,
                "event_type": self.event_type,
                "actor_subject": self.actor_subject,
                "actor_email": self.actor_email,
                "session_id": self.session_id,
                "ip_address": self.ip_address,
                "user_agent": self.user_agent,
                "outcome": self.outcome,
                "details": self.details,
            }
        )


def normalize_oidc_claims(provider: str, claims: Dict[str, Any]) -> NormalizedProfile:
    subject = str(claims.get("sub") or claims.get("user_id") or claims.get("id") or "")
    if not subject:
        raise ValueError("Missing subject claim")
    updated_at = claims.get("updated_at")
    if isinstance(updated_at, (int, float)):
        updated_at = datetime.fromtimestamp(updated_at, tz=timezone.utc).isoformat()
    return NormalizedProfile(
        provider=provider,
        subject=subject,
        email=claims.get("email"),
        email_verified=claims.get("email_verified"),
        full_name=claims.get("name"),
        given_name=claims.get("given_name"),
        family_name=claims.get("family_name"),
        picture=claims.get("picture"),
        locale=claims.get("locale"),
        updated_at=updated_at,
        raw_claims=claims,
    )
