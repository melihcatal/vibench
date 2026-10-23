import os
from urllib.parse import urlencode
from identity_client import IdentityClient, get_identity_client_config
from identity_models import OAuthTokenResponse, AuthorizationCodeExchangeRequest

def oauth_callback(payload: AuthorizationCodeExchangeRequest):
    config = get_identity_client_config()
    client = IdentityClient(config['tenant_id'], config['client_id'], config['client_secret'])
    msal_app = client.get_msal_app()

    # Prepare for token exchange
    if payload.code_verifier:
        # PKCE flow
        result = msal_app.acquire_token_by_auth_code_pkce(
            payload.code,
            payload.redirect_uri,
            payload.code_verifier,
            scopes=os.environ.get("AZURE_AD_SCOPES", "User.Read").split()
        )
    else:
        # Standard Authorization Code flow
        result = msal_app.acquire_token_by_authorization_code(
            payload.code,
            payload.redirect_uri,
            scopes=os.environ.get("AZURE_AD_SCOPES", "User.Read").split()
        )

    if "access_token" in result:
        return OAuthTokenResponse(
            access_token=result['access_token'],
            token_type=result['token_type'],
            expires_in=result['expires_in'],
            scope=result['scope'],
            refresh_token=result.get('refresh_token'),
            id_token=result.get('id_token')
        )
    else:
        raise Exception(f"Token acquisition failed: {result.get('error_description', result.get('error'))}")
