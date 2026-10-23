import hashlib
import secrets
import base64

import msal

from identity_client import load_identity_config


def _pkce_pair():
    verifier = secrets.token_urlsafe(64)
    challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode('ascii')).digest()).rstrip(b'=').decode('ascii')
    return verifier, challenge


def pkce_login(payload, config=None):
    cfg = load_identity_config(config)
    app = msal.PublicClientApplication(
        cfg.client_id,
        authority=f'{cfg.authority_host}/{cfg.tenant_id}',
    )
    verifier, challenge = _pkce_pair()
    url = app.get_authorization_request_url(
        cfg.scopes,
        redirect_uri=payload['redirect_uri'],
        code_challenge=challenge,
        code_challenge_method='S256',
        state=payload.get('state') or secrets.token_urlsafe(32),
    )
    return {'authorization_url': url, 'code_verifier': verifier}
