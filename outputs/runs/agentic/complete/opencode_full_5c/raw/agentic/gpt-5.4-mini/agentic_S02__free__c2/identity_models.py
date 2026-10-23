import hashlib
import base64
from dataclasses import dataclass


@dataclass
class LoginRequest:
    state: str
    code_challenge: str = ""


@dataclass
class TokenResponse:
    access_token: str = ""
    id_token: str = ""
    refresh_token: str = ""
    token_type: str = "Bearer"
    expires_in: int = 0


def normalize_claims(raw: dict) -> dict:
    return {
        "subject": raw.get("sub") or raw.get("id") or "",
        "email": raw.get("email") or raw.get("preferred_username") or "",
        "name": raw.get("name") or raw.get("displayName") or "",
        "given_name": raw.get("given_name") or raw.get("first_name") or "",
        "family_name": raw.get("family_name") or raw.get("last_name") or "",
        "picture": raw.get("picture") or raw.get("avatar_url") or "",
    }


def pkce_code_challenge(code_verifier: str) -> str:
    digest = hashlib.sha256(code_verifier.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(digest).decode("utf-8").rstrip("=")
