from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def compact_dict(values: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in values.items() if value is not None}


@dataclass(slots=True)
class OAuthStartRequest:
    state: str
    redirect_uri: str
    scope: str = "openid profile email"
    prompt: str | None = None
    nonce: str | None = None
    login_hint: str | None = None

    def to_params(self) -> dict[str, str]:
        return compact_dict(
            {
                "state": self.state,
                "redirect_uri": self.redirect_uri,
                "scope": self.scope,
                "prompt": self.prompt,
                "nonce": self.nonce,
                "login_hint": self.login_hint,
            }
        )


@dataclass(slots=True)
class PKCELoginRequest(OAuthStartRequest):
    code_challenge: str = ""
    code_challenge_method: str = "S256"

    def to_params(self) -> dict[str, str]:
        params = super().to_params()
        params.update(
            {
                "code_challenge": self.code_challenge,
                "code_challenge_method": self.code_challenge_method,
            }
        )
        return params


@dataclass(slots=True)
class CallbackRequest:
    code: str
    redirect_uri: str
    state: str | None = None
    code_verifier: str | None = None


@dataclass(slots=True)
class TokenSet:
    access_token: str
    token_type: str
    expires_in: int | None = None
    refresh_token: str | None = None
    id_token: str | None = None
    scope: str | None = None
    raw: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "TokenSet":
        return cls(
            access_token=payload["access_token"],
            token_type=payload.get("token_type", "Bearer"),
            expires_in=payload.get("expires_in"),
            refresh_token=payload.get("refresh_token"),
            id_token=payload.get("id_token"),
            scope=payload.get("scope"),
            raw=payload,
        )

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        return compact_dict(data)


@dataclass(slots=True)
class NormalizedProfile:
    provider: str
    subject: str
    email: str | None = None
    email_verified: bool | None = None
    full_name: str | None = None
    given_name: str | None = None
    family_name: str | None = None
    picture: str | None = None
    locale: str | None = None
    updated_at: str = field(default_factory=utc_now_iso)
    raw: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return compact_dict(asdict(self))


@dataclass(slots=True)
class AuditEvent:
    event_id: str
    user_id: str
    provider: str
    action: str
    status: str
    ip_address: str | None = None
    user_agent: str | None = None
    notes: str | None = None
    timestamp: str = field(default_factory=utc_now_iso)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return compact_dict(asdict(self))


@dataclass(slots=True)
class AuditSummary:
    total_events: int
    success_count: int
    failure_count: int
    unique_users: int
    actions: dict[str, int]
    providers: dict[str, int]
    generated_at: str = field(default_factory=utc_now_iso)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
