from dataclasses import dataclass, asdict
from typing import Any, Dict, Optional
import json


@dataclass
class OAuthLoginRequest:
    issuer: str
    client_id: str
    redirect_uri: str
    scope: str = "openid profile email"
    state: Optional[str] = None
    code_challenge: Optional[str] = None
    code_challenge_method: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class OAuthTokenResponse:
    access_token: str
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_type: Optional[str] = None
    expires_in: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def normalize_claims(raw: Dict[str, Any]) -> Dict[str, Any]:
    email = raw.get("email") or raw.get("preferred_username") or raw.get("upn")
    name = raw.get("name") or raw.get("given_name") or raw.get("nickname")
    sub = raw.get("sub") or raw.get("user_id") or raw.get("id")
    return {
        "subject": sub,
        "email": email,
        "name": name,
        "provider": raw.get("iss") or raw.get("provider") or raw.get("issuer"),
        "raw": raw,
    }


def serialize_payload(value: Dict[str, Any]) -> str:
    return json.dumps(value, separators=(",", ":"), sort_keys=True)
