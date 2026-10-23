
class FederatedLoginRequest:
    """
    Represents a request for a federated login flow.
    """
    def __init__(self, provider: str, redirect_url: str):
        self.provider = provider
        self.redirect_url = redirect_url

class FederatedLoginResponse:
    """
    Represents a response from a federated login flow.
    """
    def __init__(self, user_id: str, email: str, access_token: str):
        self.user_id = user_id
        self.email = email
        self.access_token = access_token

def normalize_federated_data(raw_data: dict) -> dict:
    """
    Normalizes raw data received from a federated identity provider.

    Args:
        raw_data: A dictionary containing raw user data from the identity provider.

    Returns:
        A dictionary containing normalized user data with consistent keys.
    """
    normalized_data = {
        "user_id": raw_data.get("sub") or raw_data.get("id"),
        "email": raw_data.get("email"),
        "first_name": raw_data.get("given_name"),
        "last_name": raw_data.get("family_name"),
    }
    return {k: v for k, v in normalized_data.items() if v is not None}
