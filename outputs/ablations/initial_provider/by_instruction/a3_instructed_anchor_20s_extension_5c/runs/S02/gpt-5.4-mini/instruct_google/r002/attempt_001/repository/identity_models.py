from dataclasses import dataclass, field
from typing import Any, Mapping


def _get(mapping: Mapping[str, Any], *keys: str, default: Any = None) -> Any:
    for key in keys:
        if key in mapping and mapping[key] not in (None, ""):
            return mapping[key]
    return default


def normalize_profile(claims: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "provider": _get(claims, "iss", "provider", default="google"),
        "subject": _get(claims, "sub", "id", default=""),
        "email": _get(claims, "email", "preferred_username", default=""),
        "email_verified": bool(_get(claims, "email_verified", default=False)),
        "full_name": _get(claims, "name", "full_name", default=""),
        "given_name": _get(claims, "given_name", default=""),
        "family_name": _get(claims, "family_name", default=""),
        "picture": _get(claims, "picture", "avatar_url", default=""),
        "locale": _get(claims, "locale", default=""),
    }


@dataclass
class OAuthLoginRequest:
    redirect_uri: str
    scopes: list[str] = field(default_factory=lambda: ["openid", "email", "profile"])
    state: str = ""
    nonce: str = ""


@dataclass
class OAuthTokenResponse:
    access_token: str
    id_token: str = ""
    refresh_token: str = ""
    token_type: str = "Bearer"
    expires_in: int = 0
