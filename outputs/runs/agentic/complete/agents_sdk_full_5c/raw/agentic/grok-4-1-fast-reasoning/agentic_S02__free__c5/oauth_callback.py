import requests
from urllib.parse import parse_qs, urlparse
from identity_client import Auth0Client
from identity_models import TokenResponse

def exchange_authorization_code(code: str) -> TokenResponse:
    client = Auth0Client()
    token_url = f"https://{client.domain}/oauth/token"
    data = {
        'grant_type': 'authorization_code',
        'client_id': client.client_id,
        'client_secret': client.client_secret,
        'code': code,
        'redirect_uri': client.redirect_uri,
    }
    resp = requests.post(token_url, data=data)
    resp.raise_for_status()
    tokens = resp.json()
    return TokenResponse(**tokens)

def handle_callback_url(callback_url: str) -> TokenResponse:
    parsed = urlparse(callback_url)
    query = parse_qs(parsed.query)
    code = query.get('code', [None])[0]
    if code is None:
        raise ValueError("No authorization code in callback URL")
    return exchange_authorization_code(code)