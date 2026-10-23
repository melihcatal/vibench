import os
from identity_client import IdentityClient
from identity_models import RefreshRequest, RefreshResponse

# Configuration for Auth0 (environment variables)
AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
AUTH0_CLIENT_ID = os.getenv('AUTH0_CLIENT_ID')
AUTH0_CLIENT_SECRET = os.getenv('AUTH0_CLIENT_SECRET')

def refresh_session(refresh_token: str) -> RefreshResponse:
    """Refresh an expired Auth0 session and return a new access token."""
    client = IdentityClient(auth0_domain=AUTH0_DOMAIN,
                            auth0_client_id=AUTH0_CLIENT_ID,
                            auth0_client_secret=AUTH0_CLIENT_SECRET)
    payload = RefreshRequest(refresh_token=refresh_token)
    resp = client.refresh_access_token(payload)
    return RefreshResponse(
        access_token=resp.get('access_token'),
        expires_in=resp.get('expires_in')
    )
