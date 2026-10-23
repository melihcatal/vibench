import secrets
from urllib.parse import urlencode

def pkce_login(payload, config):
    code_verifier = secrets.token_urlsafe(32)
    code_challenge = secrets.token_urlsafe(32)
    domain = f"https://{config['domain_prefix']}.auth.{config['region']}.amazoncognito.com"
    query = {
        'response_type': 'code',
        'client_id': config['client_id'],
        'redirect_uri': payload['redirect_uri'],
        'scope': 'openid email profile',
        'code_challenge': code_challenge,
        'code_challenge_method': 'S256'
    }
    return {
        'authorization_url': domain + '/oauth2/authorize?' + urlencode(query),
        'code_verifier': code_verifier
    }