from __future__ import annotations
from typing import Any, Dict, Optional
from dataclasses import dataclass, asdict

@dataclass
class AuthCodeResponse:
    '''Parsed response from an authorization code exchange.'''
    access_token: Optional[str] = None
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    expires_in: Optional[int] = None
    token_type: Optional[str] = None
    # Provider-specific fields
    scope: Optional[str] = None

    def asdict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class TokenSet:
    '''Set of tokens returned after authentication.'''
    access_token: str
    id_token: str
    refresh_token: Optional[str] = None
    expires_at: Optional[int] = None  # Unix epoch seconds

    def as_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class ProfileClaims:
    '''Normalized user profile claims after federation.'''
    user_id: str
    email: Optional[str] = None
    email_verified: Optional[bool] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    picture_url: Optional[str] = None
    # Add other standardized fields as needed

    def asdict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class AuthErrorResponse:
    '''Error payload received during authentication failures.'''
    error: str
    error_description: Optional[str] = None

# Additional helpers (e.g., Claim Normalizer) can be added here later.
