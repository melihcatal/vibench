import secrets
from urllib.parse import urlencode

from.identity_client import IdentityClient


def pkce_login(payload, config=None):
    config = config or {}
    code_verifier = secrets.token_urlsafe(32)
    code_challenge = secrets.token_urlsafe(32)
    client = IdentityClient(config)
    query = {
        'response_type': 'code',
        'client_id': config['client_id'],
        'redirect_uri': payload['redirect_uri'],
        'scope': 'openid email profile',
        'code_challenge': code_challenge,
        'code_challenge_method': 'S256'
    }
    authorization_url = client.get_authorization_url(query)
    return {
        'authorization_url': authorization_url,
        'code_verifier': code_verifier
    }