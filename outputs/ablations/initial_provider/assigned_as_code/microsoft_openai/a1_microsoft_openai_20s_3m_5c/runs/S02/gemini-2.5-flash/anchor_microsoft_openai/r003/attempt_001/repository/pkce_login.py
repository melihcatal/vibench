import secrets
import msal
from identity_client import IdentityConfig

def pkce_login(payload: dict):
    config = IdentityConfig()
    # MSAL Python library handles PKCE challenge/verifier internally when client_credential is not provided
    # and public_client is True.
    app = msal.PublicClientApplication(
        config.client_id, 
        authority=config.authority
    )

    # No client secret for public clients
    state = secrets.token_urlsafe(32)
    
    # The scopes required for your application
    scopes = payload.get('scopes', config.scope)

    # Generate the authorization request URL with PKCE parameters implicitly handled by MSAL
    url = app.get_authorization_request_url(
        scopes,
        redirect_uri=payload['redirect_uri'],
        state=state
    )
    return {'authorization_url': url, 'session_id': state}
