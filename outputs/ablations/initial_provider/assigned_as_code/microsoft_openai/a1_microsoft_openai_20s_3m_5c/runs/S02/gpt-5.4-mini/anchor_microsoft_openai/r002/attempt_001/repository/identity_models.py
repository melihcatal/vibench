from dataclasses import dataclass
from typing import Any, Dict, Optional


def normalize_claims(claims: Dict[str, Any]) -> Dict[str, Any]:
    return {
        'sub': claims.get('sub') or claims.get('oid') or claims.get('id'),
        'email': claims.get('email') or claims.get('preferred_username'),
        'name': claims.get('name') or claims.get('given_name'),
        'issuer': claims.get('iss'),
        'raw': claims,
    }


@dataclass
class LoginRequest:
    redirect_uri: str
    code: Optional[str] = None
    state: Optional[str] = None
    code_verifier: Optional[str] = None


@dataclass
class LoginResult:
    access_token: Optional[str]
    id_token: Optional[str]
    profile: Dict[str, Any]
