import secrets
import hashlib
import base64
import requests
from typing import Optional, Tuple
from urllib.parse import urlencode
from identity_client import GoogleIdentityClient
from identity_models import TokenResponse


def generate_pkce_pair() -> Tuple[str, str]:
    code_verifier = (
        base64.urlsafe_b64encode(secrets.token_bytes(32)).decode("ascii").rstrip("=")
    )
    code_challenge_data = hashlib.sha256(code_verifier.encode("ascii")).digest()
    code_challenge = (
        base64.urlsafe_b64encode(code_challenge_data).decode("ascii").rstrip("=")
    )
    return code_verifier, code_challenge


def generate_pkce_auth_url(code_verifier: str, state: Optional[str] = None) -> str:
    code_challenge_data = hashlib.sha256(code_verifier.encode("ascii")).digest()
    code_challenge = (
        base64.urlsafe_b64encode(code_challenge_data).decode("ascii").rstrip("=")
    )
    client = GoogleIdentityClient()
    params = {
        "client_id": client.CLIENT_ID,
        "redirect_uri": client.REDIRECT_URI,
        "scope": " ".join(client.SCOPES),
        "response_type": "code",
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    }
    if state:
        params["state"] = state
    query_string = urlencode(params)
    return f"{client.AUTH_URL}?{query_string}"


def exchange_pkce_code(code: str, code_verifier: str) -> TokenResponse:
    client = GoogleIdentityClient()
    data = {
        "client_id": client.CLIENT_ID,
        "code": code,
        "code_verifier": code_verifier,
        "grant_type": "authorization_code",
        "redirect_uri": client.REDIRECT_URI,
    }
    response = requests.post(client.TOKEN_URL, data=data)
    response.raise_for_status()
    tokens = response.json()
    return TokenResponse(**tokens)
