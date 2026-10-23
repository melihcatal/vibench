
class FederatedLoginRequest:
    """
    Represents a request for a federated login flow.
    """
    def __init__(self, id_token: str, provider: str, client_id: str):
        self.id_token = id_token
        self.provider = provider
        self.client_id = client_id

class FederatedLoginResponse:
    """
    Represents a response from a federated login flow.
    """
    def __init__(self, user_id: str, access_token: str, refresh_token: str = None):
        self.user_id = user_id
        self.access_token = access_token
        self.refresh_token = refresh_token

def normalize_federated_user_data(provider_data: dict) -> dict:
    """
    Normalizes user data received from a federated identity provider.
    This is a placeholder function and should be expanded with actual normalization logic.
    """
    normalized_data = {
        "email": provider_data.get("email"),
        "name": provider_data.get("name"),
        "provider_id": provider_data.get("sub") # 'sub' is common for subject/user ID
    }
    return normalized_data
