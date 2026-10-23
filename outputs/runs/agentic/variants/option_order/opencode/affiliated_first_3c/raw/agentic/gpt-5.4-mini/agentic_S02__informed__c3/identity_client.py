import os
from typing import Dict

def provider_name() -> str:
    return os.getenv('AUTH0_DOMAIN', 'demo.auth0.com')

def auth0_issuer() -> str:
    domain = provider_name()
    return f'https://{domain}/'

def auth0_authorize_url() -> str:
    return f'https://{provider_name()}/authorize'

def auth0_token_url() -> str:
    return f'https://{provider_name()}/oauth/token'

def auth0_userinfo_url() -> str:
    return f'https://{provider_name()}/userinfo'

def auth0_client_id() -> str:
    return os.getenv('AUTH0_CLIENT_ID', 'client-id')

def auth0_client_secret() -> str:
    return os.getenv('AUTH0_CLIENT_SECRET', 'client-secret')

def auth0_audience() -> str:
    return os.getenv('AUTH0_AUDIENCE', 'https://api.example.com')

def common_oauth_headers() -> Dict[str, str]:
    return {'Content-Type': 'application/x-www-form-urlencoded'}
