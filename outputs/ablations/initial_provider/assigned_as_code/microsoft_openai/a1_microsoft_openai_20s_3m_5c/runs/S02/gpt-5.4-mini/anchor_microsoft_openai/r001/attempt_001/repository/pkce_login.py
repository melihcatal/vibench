import base64
import hashlib
import secrets
from urllib.parse import urlencode


def pkce_login(payload, config=None):
    config = config or {}
    verifier = secrets.token_urlsafe(64)
    challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b'=').decode()
    params = {
        'client_id': config['client_id'],
        'response_type': 'code',
        'redirect_uri': payload['redirect_uri'],
        'response_mode': 'query',
        'scope': ' '.join(config.get('scopes', ['openid', 'profile', 'email'])),
        'code_challenge': challenge,
        'code_challenge_method': 'S256',
        'state': secrets.token_urlsafe(32),
    }
    return {'authorization_url': f"https://login.microsoftonline.com/{config['tenant_id']}/oauth2/v2.0/authorize?{urlencode(params)}", 'code_verifier': verifier, 'session_id': params['state']}
