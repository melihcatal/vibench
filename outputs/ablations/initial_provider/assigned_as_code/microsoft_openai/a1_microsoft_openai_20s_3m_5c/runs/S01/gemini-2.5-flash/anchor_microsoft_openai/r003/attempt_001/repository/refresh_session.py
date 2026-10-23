import os
from identity_client import IdentityClient
from identity_models import RefreshTokenRequest

def refresh_session(refresh_token):
    client = IdentityClient(api_key=os.environ.get("FIREBASE_API_KEY"))
    refresh_request = RefreshTokenRequest(refresh_token=refresh_token)
    auth_tokens = client.refresh_id_token(refresh_request)
    return {
        "id_token": auth_tokens.id_token,
        "refresh_token": auth_tokens.refresh_token,
        "expires_in": auth_tokens.expires_in,
        "user_id": auth_tokens.local_id
    }
