
"""
Local request, response, and normalization helpers for Federated Login Flow.
"""

from dataclasses import dataclass
from typing import Any, Dict, Optional

@dataclass
class FederatedLoginRequest:
    """
    Represents a request for a federated login.
    """
    id_token: str
    provider: str
    redirect_uri: Optional[str] = None
    state: Optional[str] = None

@dataclass
class FederatedLoginResponse:
    """
    Represents a response after a successful federated login.
    """
    user_id: str
    email: str
    display_name: Optional[str] = None
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    id_token: Optional[str] = None

def normalize_user_data(provider_data: Dict[str, Any], provider_name: str) -> Dict[str, Any]:
    """
    Normalizes user data received from different identity providers into a common format.

    Args:
        provider_data: A dictionary containing user data from the identity provider.
        provider_name: The name of the identity provider (e.g., "google", "facebook").

    Returns:
        A dictionary containing normalized user data.
    """
    normalized_data = {
        "user_id": provider_data.get("sub") or provider_data.get("id"),
        "email": provider_data.get("email"),
        "display_name": provider_data.get("name") or provider_data.get("preferred_username"),
    }

    # Provider-specific adjustments can be made here
    if provider_name == "google":
        normalized_data["picture"] = provider_data.get("picture")
    elif provider_name == "facebook":
        normalized_data["first_name"] = provider_data.get("first_name")
        normalized_data["last_name"] = provider_data.get("last_name")

    return {k: v for k, v in normalized_data.items() if v is not None} # Remove None values
