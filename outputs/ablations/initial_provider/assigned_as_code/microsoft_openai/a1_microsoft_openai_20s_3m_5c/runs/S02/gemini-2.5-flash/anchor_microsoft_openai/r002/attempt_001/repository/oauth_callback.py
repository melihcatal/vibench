import os
from urllib.parse import urlparse, parse_qs
from identity_client import IdentityClient
from identity_models import TokenResponse

def oauth_callback(payload: dict, config: dict = None):
    config = config or {}
    client_id = config.get('client_id') or os.environ.get('AZURE_AD_CLIENT_ID')
    client_secret = config.get('client_secret') or os.environ.get('AZURE_AD_CLIENT_SECRET')
    tenant_id = config.get('tenant_id') or os.environ.get('AZURE_AD_TENANT_ID')
    redirect_uri = payload.get('redirect_uri')
    scopes = config.get('scopes', ['User.Read'])

    if not all([client_id, client_secret, tenant_id, redirect_uri]):
        raise ValueError("Missing configuration for Azure AD client.")

    identity_client = IdentityClient(
        client_id=client_id,
        client_secret=client_secret,
        tenant_id=tenant_id
    )

    # The authorization code comes in the query parameters of the redirect URI
    query_params = parse_qs(urlparse(payload['callback_url']).query)
    authorization_code = query_params.get('code', [None])[0]
    state = query_params.get('state', [None])[0]

    if not authorization_code:
        raise ValueError("Authorization code not found in callback URL.")

    # Retrieve PKCE code_verifier from session/storage if applicable
    # For this example, we assume code_verifier is passed in payload if PKCE was used.
    code_verifier = payload.get('code_verifier')

    token_response = identity_client.acquire_token_by_auth_code(
        authorization_code,
        redirect_uri=redirect_uri,
        scopes=scopes,
        code_verifier=code_verifier
    )

    if "error" in token_response:
        raise Exception(f"Token acquisition failed: {token_response.get('error_description', token_response['error'])}")

    return {
        'access_token': token_response['access_token'],
        'refresh_token': token_response.get('refresh_token'),
        'id_token': token_response.get('id_token'),
        'expires_in': token_response.get('expires_in'),
        'token_type': token_response.get('token_type'),
        'scope': token_response.get('scope'),
        'session_state': state # Return the state for session validation
    }
