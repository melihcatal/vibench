import webbrowser
import urllib.parse
import requests
from identity_client import (
    GOOGLE_AUTH_URL, GOOGLE_CLIENT_ID, GOOGLE_SCOPES, GOOGLE_TOKEN_URL,
    generate_pkce_pair, build_auth_params
)
from identity_models import TokenResponse

def start_pkce_login(redirect_uri: str, state: str = None) -> tuple[str, str]:
    code_verifier, code_challenge = generate_pkce_pair()
    params = build_auth_params(GOOGLE_CLIENT_ID, redirect_uri, GOOGLE_SCOPES, state, code_challenge)
    query_string = urllib.parse.urlencode(params)
    auth_url = f"{GOOGLE_AUTH_URL}?{query_string}"
    print(f"Opening PKCE authorization URL: {auth_url}")
    webbrowser.open(auth_url)
    return auth_url, code_verifier

def exchange_pkce_code(code: str, redirect_uri: str, code_verifier: str) -> TokenResponse:
    data = {
        'client_id': GOOGLE_CLIENT_ID,
        'code': code,
        'code_verifier': code_verifier,
        'grant_type': 'authorization_code',
        'redirect_uri': redirect_uri,
    }
    response = requests.post(GOOGLE_TOKEN_URL, data=data)
    response.raise_for_status()
    token_data = response.json()
    return TokenResponse.from_response(token_data)
