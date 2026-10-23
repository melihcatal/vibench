from dataclasses import dataclass, field
from typing import Optional, Dict

@dataclass
class AuthCodeExchangeRequest:
    code: str
    redirect_uri: str
    client_id: str
    code_verifier: Optional[str] = None

@dataclass
class AuthTokensResponse:
    id_token: str
    access_token: str
    refresh_token: Optional[str] = None
    expires_in: Optional[int] = None
    token_type: Optional[str] = None

@dataclass
class UserProfileClaims:
    username: str
    attributes: Dict[str, str] = field(default_factory=dict)
    provider: str
    email: Optional[str] = None
    name: Optional[str] = None

    def normalize(self) -> Dict[str, str]:
        """
        Normalizes the user profile claims into a flat dictionary.
        """
        normalized = {
            "username": self.username,
            "provider": self.provider
        }
        if self.email: normalized["email"] = self.email
        if self.name: normalized["name"] = self.name
        normalized.update(self.attributes)
        return normalized
