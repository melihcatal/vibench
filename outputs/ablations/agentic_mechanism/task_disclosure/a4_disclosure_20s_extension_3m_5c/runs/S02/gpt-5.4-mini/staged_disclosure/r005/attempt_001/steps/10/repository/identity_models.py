from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Optional


def _clean_str(value: Any) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, str):
        stripped = value.strip()
        return stripped or None
    return str(value).strip() or None


def _clean_mapping(value: Any) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        return {}
    return dict(value)


@dataclass(slots=True)
class FederatedLoginRequest:
    provider: str
    assertion: str
    redirect_uri: Optional[str] = None
    state: Optional[str] = None
    nonce: Optional[str] = None
    scope: tuple[str, ...] = field(default_factory=tuple)
    claims: dict[str, Any] = field(default_factory=dict)

    def normalized(self) -> "FederatedLoginRequest":
        return FederatedLoginRequest(
            provider=_clean_str(self.provider) or "",
            assertion=_clean_str(self.assertion) or "",
            redirect_uri=_clean_str(self.redirect_uri),
            state=_clean_str(self.state),
            nonce=_clean_str(self.nonce),
            scope=tuple(
                s for s in (_clean_str(item) for item in self.scope) if s
            ),
            claims=_clean_mapping(self.claims),
        )


@dataclass(slots=True)
class FederatedLoginResponse:
    access_token: Optional[str] = None
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_type: str = "Bearer"
    expires_in: Optional[int] = None
    subject: Optional[str] = None
    provider: Optional[str] = None
    profile: dict[str, Any] = field(default_factory=dict)
    raw: dict[str, Any] = field(default_factory=dict)

    def normalized(self) -> "FederatedLoginResponse":
        return FederatedLoginResponse(
            access_token=_clean_str(self.access_token),
            id_token=_clean_str(self.id_token),
            refresh_token=_clean_str(self.refresh_token),
            token_type=_clean_str(self.token_type) or "Bearer",
            expires_in=int(self.expires_in) if self.expires_in is not None else None,
            subject=_clean_str(self.subject),
            provider=_clean_str(self.provider),
            profile=_clean_mapping(self.profile),
            raw=_clean_mapping(self.raw),
        )


def normalize_federated_login_request(data: Mapping[str, Any]) -> FederatedLoginRequest:
    return FederatedLoginRequest(
        provider=_clean_str(data.get("provider")) or "",
        assertion=_clean_str(data.get("assertion")) or "",
        redirect_uri=_clean_str(data.get("redirect_uri")),
        state=_clean_str(data.get("state")),
        nonce=_clean_str(data.get("nonce")),
        scope=tuple(
            s
            for s in (
                _clean_str(item)
                for item in (data.get("scope") or ())
            )
            if s
        ),
        claims=_clean_mapping(data.get("claims")),
    )


def normalize_federated_login_response(data: Mapping[str, Any]) -> FederatedLoginResponse:
    return FederatedLoginResponse(
        access_token=_clean_str(data.get("access_token")),
        id_token=_clean_str(data.get("id_token")),
        refresh_token=_clean_str(data.get("refresh_token")),
        token_type=_clean_str(data.get("token_type")) or "Bearer",
        expires_in=int(data["expires_in"]) if data.get("expires_in") is not None else None,
        subject=_clean_str(data.get("subject")),
        provider=_clean_str(data.get("provider")),
        profile=_clean_mapping(data.get("profile")),
        raw=dict(data),
    )
