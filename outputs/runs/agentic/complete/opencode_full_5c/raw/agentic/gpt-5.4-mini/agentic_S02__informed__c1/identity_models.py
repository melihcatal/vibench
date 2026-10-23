import dataclasses
from typing import Any, Dict, Iterable, Optional


@dataclasses.dataclass
class OAuthLoginRequest:
    redirect_uri: str
    scope: str = "openid profile email"
    state: str = ""
    nonce: str = ""
    code_verifier: str = ""
    code_challenge: str = ""
    code_challenge_method: str = "S256"


@dataclasses.dataclass
class OAuthTokenResponse:
    access_token: str
    id_token: str = ""
    refresh_token: str = ""
    token_type: str = "Bearer"
    expires_in: int = 0
    raw: Optional[Dict[str, Any]] = None


def normalize_profile_claims(claims: Dict[str, Any]) -> Dict[str, Any]:
    name = (
        claims.get("name")
        or claims.get("preferred_username")
        or claims.get("email")
        or ""
    )
    given_name = claims.get("given_name") or ""
    family_name = claims.get("family_name") or ""
    email = claims.get("email") or claims.get("upn") or ""
    return {
        "sub": claims.get("sub", ""),
        "name": name,
        "given_name": given_name,
        "family_name": family_name,
        "email": email,
        "email_verified": bool(claims.get("email_verified", False)),
        "issuer": claims.get("iss", ""),
        "raw": claims,
    }


def safe_audience(audience: Iterable[str]) -> list[str]:
    return [item for item in audience if item]
