from identity_client import IdentityClient
from identity_models import RefreshSessionRequest

def refresh_session(refresh_token: str):
    client = IdentityClient()
    request = RefreshSessionRequest(refresh_token=refresh_token)
    response = client.refresh_session(request)
    return response
