from typing import Optional, Dict, Any
from dataclasses import dataclass

@dataclass
class FederatedLoginEvent:
    """Represents a federated login event for auditing purposes."""
    timestamp: str
    provider: str
    user_id: str
    session_id: str
    event_type: str # e.g., "LOGIN_SUCCESS", "LOGIN_FAILURE", "TOKEN_EXCHANGE"
    details: Dict[str, Any]
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None

@dataclass
class NormalizedUserProfile:
    """Standardized user profile structure after federated login."""
    provider: str
    id: str
    display_name: Optional[str] = None
    email: Optional[str] = None
    picture: Optional[str] = None
    raw_claims: Optional[Dict[str, Any]] = None # Original claims from the IdP

@dataclass
class ConsentStatement:
    """Represents a consent statement from an identity provider."""
    idp_text: str
    language: str
    version: str
    timestamp: str
    scope: Optional[str] = None
    client_id: Optional[str] = None

# Example usage in other files:
# from identity_models import NormalizedUserProfile, FederatedLoginEvent
# profile = NormalizedUserProfile(provider="google", id="123", email="test@example.com")
# event = FederatedLoginEvent(timestamp="...", provider="google", user_id="123", ...)
