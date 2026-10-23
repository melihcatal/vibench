
class FederatedLoginRequest:
    def __init__(self, id_token: str, provider: str):
        self.id_token = id_token
        self.provider = provider

class FederatedLoginResponse:
    def __init__(self, user_id: str, email: str, access_token: str):
        self.user_id = user_id
        self.email = email
        self.access_token = access_token

def normalize_federated_user_data(provider_data: dict) -> dict:
    """
    Normalizes user data received from different federated identity providers.
    This is a placeholder and would need to be expanded based on actual provider data structures.
    """
    normalized_data = {
        "user_id": provider_data.get("sub"),  # Example for OpenID Connect 'sub' claim
        "email": provider_data.get("email"),
        "first_name": provider_data.get("given_name"),
        "last_name": provider_data.get("family_name"),
    }
    return normalized_data
