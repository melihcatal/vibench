import hashlib
import base64
import secrets

import msal

from identity_client import load_identity_config, default_scopes


def _challenge(verifier: str) -> str:
    digest = hashlib.sha256(verifier.encode('utf-8')).digest()
    return base64.urlsafe_b64encode(digest).decode('utf-8').rstrip('=')


def pkce_login(payload, config=None):
    config = config or load_identity_config()
    verifier = secrets.token_urlsafe(64)
    app = msal.PublicClientApplication(
        config['client_id'],
        authority=f"https://login.microsoftonline.com/{config['tenant_id']}",
    )
    flow = app.initiate_auth_code_flow(scopes=config.get('scopes', default_scopes()), redirect_uri=payload['redirect_uri'])
    flow['code_verifier'] = verifier
    flow['code_challenge'] = _challenge(verifier)
    return {'authorization_url': flow['auth_uri'], 'state': flow['state'], 'code_verifier': verifier}
