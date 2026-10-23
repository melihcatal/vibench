import os
from identity_client import IdentityClient
from identity_models import TokenRefreshPayload, TokenRefreshResponse

# Auth0 token endpoint for refreshing expired access tokens
auth0_domain = os.getenv('AUTH0_DOMAIN')
auth0_client_id = os.getenv('AUTH0_CLIENT_ID')

client = IdentityClient(
    base_url=f'https://{auth0_domain}',
    client_id=auth0_client_id,
    audience='https://{auth0_domain}/api/v2/'
)

def refresh_session(refresh_token: str) -> TokenRefreshResponse:
    """Refresh an expired session using Auth0 /oauth/token endpoint.
    Returns new access and refresh tokens.
    """
    payload = TokenRefreshPayload(
        grant_type='refresh_token',
        refresh_token=refresh_token,
        client_id=auth0_client_id,
        audience='https://{auth0_domain}/api/v2/'
    )
    # Identify provider directly in the call
    response = client.refresh_token(payload, provider='auth0')
    return response

# Example usage (not executed):
# new_tokens = refresh_session(old_refresh_token)
# print('New Access Token:', new_tokens.access_token)
