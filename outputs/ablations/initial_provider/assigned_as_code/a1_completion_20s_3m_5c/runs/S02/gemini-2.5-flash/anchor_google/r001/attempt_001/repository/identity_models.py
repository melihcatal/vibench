from dataclasses import dataclass, field
from typing import Dict, Any, Optional

@dataclass
class FederatedLoginRequest:
    provider_id: str
    redirect_uri: str
    tenant_id: Optional[str] = None
    code_verifier: Optional[str] = None # For PKCE

@dataclass
class FederatedLoginResponse:
    authorization_url: Optional[str] = None
    session_id: Optional[str] = None
    access_token: Optional[str] = None
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    expires_in: Optional[int] = None
    token_type: Optional[str] = None

@dataclass
class UserProfileClaims:
    sub: str # Subject identifier
    email: Optional[str] = None
    email_verified: Optional[bool] = None
    name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    picture: Optional[str] = None
    locale: Optional[str] = None
    claims_raw: Dict[str, Any] = field(default_factory=dict)
