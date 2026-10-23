import os
import msal
from identity_client import IdentityConfig
from identity_models import AuthCodeExchangeRequest, TokenResponse

def oauth_callback(payload: AuthCodeExchangeRequest):
    config = IdentityConfig()
    app = msal.ConfidentialClientApplication(
        config.client_id, 
        authority=config.authority,
        client_credential=config.client_secret
    )

    result = app.acquire_token_by_authorization_code(
        payload.code,
        scopes=config.scope,
        redirect_uri=payload.redirect_uri
    )
    
    if "error" in result:
        raise Exception(f"Token exchange failed: {result.get('error_description')}")

    return TokenResponse(
        access_token=result['access_token'],
        refresh_token=result.get('refresh_token'),
        id_token=result.get('id_token'),
        expires_in=result.get('expires_in'),
        token_type=result.get('token_type'),
        scope=result.get('scope')
    )
