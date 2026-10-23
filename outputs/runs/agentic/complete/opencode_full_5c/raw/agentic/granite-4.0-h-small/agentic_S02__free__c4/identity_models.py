from dataclasses import dataclass
from typing import Optional, Dict, Any


class ClaimNormalization:
    """Helper for mapping provider‑specific claim names to normalized ones."""

    sub = "sub"
    email = "email"
    email_verified = "email_verified"
    name = "name"
    nickname = "nickname"
    picture = "picture"
    updated_at = "updated_at"


@dataclass
class FederatedProfile:
    user_id: Optional[str] = None
    email: Optional[str] = None
    email_verified: Optional[bool] = None
    name: Optional[str] = None
    nickname: Optional[str] = None
    picture: Optional[str] = None
    updated_at: Optional[str] = None
    # Additional custom claims can be added as dict later
    extra: Optional[Dict[str, Any]] = None

    def as_dict(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "email": self.email,
            "email_verified": self.email_verified,
            "name": self.name,
            "nickname": self.nickname,
            "picture": self.picture,
            "updated_at": self.updated_at,
            **(self.extra or {}),
        }


@dataclass
class OAuthCallbackResponse:
    access_token: str
    id_token: Optional[str] = None
    token_type: Optional[str] = None
    expires_in: Optional[int] = None
    claims: Optional[Dict[str, Any]] = None


@dataclass
class PKCEChallenge:
    verifier: str
    challenge: str  # S256 encoded value
