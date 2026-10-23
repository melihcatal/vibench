
from typing import Dict, Any

class FederatedLoginRequest:
    """
    Represents a request for a federated login flow.
    """
    def __init__(self, provider: str, redirect_url: str):
        self.provider = provider
        self.redirect_url = redirect_url

    def to_dict(self) -> Dict[str, Any]:
        return {
            "provider": self.provider,
            "redirect_url": self.redirect_url
        }

class FederatedLoginResponse:
    """
    Represents a response from a federated login flow.
    """
    def __init__(self, success: bool, user_data: Dict[str, Any] = None, error_message: str = None):
        self.success = success
        self.user_data = user_data if user_data is not None else {}
        self.error_message = error_message

    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "user_data": self.user_data,
            "error_message": self.error_message
        }

def normalize_federated_user_data(provider: str, raw_user_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalizes user data received from different federated identity providers.

    Args:
        provider: The name of the identity provider (e.g., "google", "facebook").
        raw_user_data: The raw user data dictionary from the identity provider.

    Returns:
        A normalized dictionary of user data.
    """
    normalized_data = {
        "id": raw_user_data.get("id"),
        "email": raw_user_data.get("email"),
        "name": raw_user_data.get("name"),
        "provider": provider,
    }

    # Provider-specific normalization can be added here
    if provider == "google":
        normalized_data["first_name"] = raw_user_data.get("given_name")
        normalized_data["last_name"] = raw_user_data.get("family_name")
    elif provider == "facebook":
        normalized_data["profile_link"] = raw_user_data.get("link")

    return normalized_data
