from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Mapping, Optional


def normalize_claims(claims: Mapping[str, Any]) -> Dict[str, Any]:
    normalized = dict(claims)
    if "email" in normalized and isinstance(normalized["email"], str):
        normalized["email"] = normalized["email"].strip().lower()
    if "name" not in normalized:
        parts = [normalized.get("given_name"), normalized.get("family_name")]
        name = " ".join([p for p in parts if isinstance(p, str) and p.strip()])
        if name:
            normalized["name"] = name
    return normalized


@dataclass
class LoginRequest:
    redirect_uri: str
    state: str
    nonce: str
    scope: List[str] = field(default_factory=lambda: ["openid", "profile", "email"])


@dataclass
class TokenResponse:
    access_token: str
    id_token: str
    refresh_token: Optional[str] = None
    expires_in: Optional[int] = None
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ClaimsProfile:
    subject: str
    email: Optional[str] = None
    name: Optional[str] = None
    issuer: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)
