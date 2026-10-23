from dataclasses import dataclass
from typing import Any, Dict, Mapping, Optional


def _string_or_none(value: Any) -> Optional[str]:
    if isinstance(value, str):
        value = value.strip()
        return value or None
    return None


def _join_name(given_name: Any, family_name: Any) -> Optional[str]:
    parts = [part for part in [given_name, family_name] if isinstance(part, str) and part.strip()]
    if not parts:
        return None
    return " ".join(parts)


@dataclass(frozen=True)
class AuthorizationCodeRequest:
    code: str
    redirect_uri: str
    state: Optional[str] = None
    code_verifier: Optional[str] = None


@dataclass(frozen=True)
class TokenResponse:
    access_token: str
    token_type: str
    expires_in: Optional[int] = None
    refresh_token: Optional[str] = None
    id_token: Optional[str] = None
    scope: Optional[str] = None
    raw: Optional[Dict[str, Any]] = None


@dataclass(frozen=True)
class NormalizedIdentityClaims:
    subject: Optional[str]
    email: Optional[str]
    name: Optional[str]
    picture: Optional[str]
    locale: Optional[str]


def normalize_profile_claims(claims: Mapping[str, Any]) -> Dict[str, Optional[str]]:
    normalized_email = claims.get("email") or claims.get("preferred_username")
    normalized_name = claims.get("name") or _join_name(claims.get("given_name"), claims.get("family_name"))
    normalized_subject = claims.get("sub")
    normalized_picture = claims.get("picture")
    normalized_locale = claims.get("locale")
    return {
        "subject": _string_or_none(normalized_subject),
        "email": _string_or_none(normalized_email),
        "name": _string_or_none(normalized_name),
        "picture": _string_or_none(normalized_picture),
        "locale": _string_or_none(normalized_locale),
    }


def normalize_claims_object(claims: Mapping[str, Any]) -> NormalizedIdentityClaims:
    normalized = normalize_profile_claims(claims)
    return NormalizedIdentityClaims(
        subject=normalized["subject"],
        email=normalized["email"],
        name=normalized["name"],
        picture=normalized["picture"],
        locale=normalized["locale"],
    )


def build_token_response(payload: Mapping[str, Any]) -> TokenResponse:
    return TokenResponse(
        access_token=str(payload["access_token"]),
        token_type=str(payload.get("token_type", "Bearer")),
        expires_in=payload.get("expires_in"),
        refresh_token=payload.get("refresh_token"),
        id_token=payload.get("id_token"),
        scope=payload.get("scope"),
        raw=dict(payload),
    )
