from dataclasses import dataclass, asdict
from typing import Any, Dict, Optional


def normalize_claims(claims: Dict[str, Any]) -> Dict[str, Any]:
    normalized = {}
    for key, value in claims.items():
        if value is None:
            continue
        k = key.lower().replace(' ', '_')
        normalized[k] = value
    if 'sub' in claims and 'user_id' not in normalized:
        normalized['user_id'] = claims['sub']
    if 'email' in claims:
        normalized['email'] = str(claims['email']).lower()
    return normalized


@dataclass
class OAuthTokenResponse:
    access_token: str
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_type: Optional[str] = None
    expires_in: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class LoginRequest:
    redirect_uri: str
    state: str
    scope: str = 'openid profile email'


@dataclass
class CallbackRequest:
    code: str
    state: str
    redirect_uri: str
    code_verifier: Optional[str] = None
