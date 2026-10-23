import os
import hashlib
import base64
from urllib.parse import urlencode
import requests

from identity_client import IdentityClientConfig
from identity_models import TokenResponse


def generate_pkce_codes():
    code_verifier = base64.urlsafe_b64encode(os.urandom(40)).decode("utf-8")
    code_verifier = "".join(filter(str.isalnum, code_verifier))

    code_challenge = hashlib.sha256(code_verifier.encode("utf-8")).digest()
    code_challenge = (
        base64.urlsafe_b64encode(code_challenge).decode("utf-8").replace("=", "")
    )

    return code_verifier, code_challenge


def get_auth0_pkce_auth_url(code_challenge: str):
    config = IdentityClientConfig()
    params = {
        "client_id": config.AUTH0_CLIENT_ID,
        "response_type": "code",
        "scope": "openid profile email",
        "redirect_uri": config.AUTH0_REDIRECT_URI,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
        "state": "random_state_string_pkce",
    }
    authorization_url = f"https://{config.AUTH0_DOMAIN}/authorize?{urlencode(params)}"
    return authorization_url


def exchange_pkce_code_for_token(
    authorization_code: str, code_verifier: str
) -> TokenResponse:
    config = IdentityClientConfig()

    token_url = f"https://{config.AUTH0_DOMAIN}/oauth/token"

    payload = {
        "grant_type": "authorization_code",
        "code": authorization_code,
        "redirect_uri": config.AUTH0_REDIRECT_URI,
        "client_id": config.AUTH0_CLIENT_ID,
        "code_verifier": code_verifier,
    }

    response = requests.post(token_url, json=payload)
    response.raise_for_status()

    return TokenResponse(**response.json())
