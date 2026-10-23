from dataclasses import dataclass
from typing import Any


@dataclass
class LoginRequest:
    state: str
    nonce: str
    code_verifier: str | None = None
    code_challenge: str | None = None
    redirect_uri: str | None = None


@dataclass
class TokenResponse:
    access_token: str
    id_token: str | None = None
    refresh_token: str | None = None
    token_type: str | None = None
    expires_in: int | None = None


def normalize_claims(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "subject": payload.get("sub") or payload.get("user_id") or payload.get("id"),
        "email": payload.get("email"),
        "name": payload.get("name")
        or payload.get("nickname")
        or payload.get("preferred_username"),
        "given_name": payload.get("given_name"),
        "family_name": payload.get("family_name"),
        "picture": payload.get("picture"),
        "raw": payload,
    }
