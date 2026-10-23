import msal

from identity_client import load_identity_config
from identity_models import make_pkce_challenge, make_pkce_verifier


def pkce_login(payload, config=None):
    payload = dict(payload or {})
    config = load_identity_config(config)
    verifier = payload.get('code_verifier') or make_pkce_verifier()
    challenge = make_pkce_challenge(verifier)
    app = msal.PublicClientApplication(config['client_id'], authority=config['authority'])
    url = app.get_authorization_request_url(
        scopes=payload.get('scopes') or config['scopes'],
        redirect_uri=payload['redirect_uri'],
        state=payload.get('state'),
        code_challenge=challenge,
        code_challenge_method='S256',
    )
    return {'authorization_url': url, 'code_verifier': verifier, 'code_challenge': challenge}
