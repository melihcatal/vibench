import requests
import urllib.parse
from urllib.parse import urlparse, parse_qs
from identity_client import generate_pkce_pair, GOOGLE_CLIENT_ID, REDIRECT_URI, SCOPES
from identity_models import Tokens


def pkce_login_flow():
    verifier, challenge = generate_pkce_pair()
    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": " ".join(SCOPES),
        "response_type": "code",
        "code_challenge": challenge,
        "code_challenge_method": "S256",
        "prompt": "consent",
    }
    auth_url = "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode(
        params
    )
    print("Open the following URL in your browser:")
    print(auth_url)
    callback_url = input(
        "After authorization, paste the full redirect callback URL here: "
    )
    query_params = parse_qs(urlparse(callback_url).query)
    code = query_params.get("code", [None])[0]
    if not code:
        raise ValueError("Authorization failed")
    token_params = {
        "client_id": GOOGLE_CLIENT_ID,
        "code": code,
        "code_verifier": verifier,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI,
    }
    token_response = requests.post(
        "https://oauth2.googleapis.com/token", data=token_params
    )
    token_response.raise_for_status()
    tokens = token_response.json()
    return Tokens(**tokens)
