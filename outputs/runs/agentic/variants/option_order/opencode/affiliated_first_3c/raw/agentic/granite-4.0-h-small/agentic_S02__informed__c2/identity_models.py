from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional


@dataclass
class ClaimsNormalization:
    """Standardized user claims after federated login."""

    sub: str
    email: Optional[str] = None
    name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    preferred_username: Optional[str] = None
    picture: Optional[str] = None
    locale: Optional[str] = None
    # Add any other standardized claims here
    extra: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_raw_payload(cls, raw: Dict[str, Any]) -> ClaimsNormalization:
        """Map provider-specific claim names to standardized names."""
        mapping = {
            "sub": "sub",
            "email": "email",
            "name": "name",
            "preferred_username": "preferred_username",
            "given_name": "given_name",
            "family_name": "family_name",
            "picture": "picture",
            "locale": "locale",
            # Add extra mappings as needed
        }
        normalized = {key: raw.get(val) for key, val in mapping.items()}
        # Preserve any remaining fields as 'extra'
        normalized["extra"] = {k: v for k, v in raw.items() if k not in mapping}
        return cls(**normalized)


@dataclass
class IdentityConfig:
    """Local configuration holder for a specific provider."""

    client_id: str
    client_secret: Optional[str] = None
    # Add provider-specific static config values (e.g., token endpoint) if needed
    token_url: Optional[str] = None
    authorize_url: Optional[str] = None

    @classmethod
    def from_env(cls, prefix: str) -> IdentityConfig:
        """Create configuration from environment variables using the given prefix.
        Example: prefix='IBM_APPID_' reads IBM_APPID_CLIENT_ID, IBM_APPID_CLIENT_SECRET, ...
        """
        client_id = os.getenv(f"{prefix}CLIENT_ID")
        client_secret = os.getenv(f"{prefix}CLIENT_SECRET")
        instance = cls(client_id=client_id, client_secret=client_secret)
        return instance


@dataclass
class LoginRecord:
    """Model persisted audit record for the federated login flow."""

    user_id: str  # e.g., normalized sub value
    provider: str  # e.g., 'IBM App ID', 'Auth0', ...
    login_timestamp: int  # Unix epoch time (seconds)
    auth_method: str  # e.g., 'authorization_code', 'pkce'
    access_token: Optional[str] = None
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    profile: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "provider": self.provider,
            "login_timestamp": self.login_timestamp,
            "auth_method": self.auth_method,
            "access_token": self.access_token,
            "id_token": self.id_token,
            "refresh_token": self.refresh_token,
            "profile": self.profile,
        }
