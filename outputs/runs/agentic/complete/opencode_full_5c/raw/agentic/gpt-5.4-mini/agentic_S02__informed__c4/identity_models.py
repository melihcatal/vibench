import base64
import hashlib
import json
import os
import secrets
from dataclasses import dataclass, asdict
from typing import Any, Dict, Optional


def _compact_json(data: Dict[str, Any]) -> str:
    return json.dumps(data, separators=(",", ":"), sort_keys=True)


def normalize_profile_claims(claims: Dict[str, Any]) -> Dict[str, Any]:
    email = claims.get("email") or claims.get("upn") or claims.get("preferred_username")
    name = (
        claims.get("name")
        or " ".join(
            part
            for part in [claims.get("given_name"), claims.get("family_name")]
            if part
        ).strip()
    )
    return {
        "subject": claims.get("sub") or claims.get("user_id") or claims.get("id"),
        "email": email,
        "name": name or claims.get("nickname") or email,
        "issuer": claims.get("iss") or claims.get("issuer"),
        "claims": claims,
    }


@dataclass
class OAuthRequest:
    authorization_url: str
    state: str
    nonce: str
    code_verifier: Optional[str] = None
    code_challenge: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class OAuthTokenResponse:
    access_token: str
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_type: Optional[str] = None
    expires_in: Optional[int] = None
    raw: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def create_state_token(length: int = 32) -> str:
    return secrets.token_urlsafe(length)


def create_nonce(length: int = 32) -> str:
    return secrets.token_urlsafe(length)


def create_pkce_pair() -> Dict[str, str]:
    verifier = secrets.token_urlsafe(64)
    digest = hashlib.sha256(verifier.encode("utf-8")).digest()
    challenge = base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")
    return {"code_verifier": verifier, "code_challenge": challenge}


def pack_session(data: Dict[str, Any]) -> str:
    return base64.urlsafe_b64encode(_compact_json(data).encode("utf-8")).decode("ascii")


def unpack_session(value: str) -> Dict[str, Any]:
    return json.loads(base64.urlsafe_b64decode(value.encode("ascii")).decode("utf-8"))


def load_env(name: str, default: Optional[str] = None) -> Optional[str]:
    return os.environ.get(name, default)
