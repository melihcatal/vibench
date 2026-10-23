import os
import requests
from base64 import b64encode

from identity_client import OKTA_ORG_URL, OKTA_CLIENT_ID, OKTA_CLIENT_SECRET, OKTA_REDIRECT_URI

def exchange_code_for_tokens(code: str) -> dict:
    """Exchanges an authorization code for access and ID tokens with Okta."""
    token_endpoint = f"{OKTA_ORG_URL}/oauth2/default/v1/token"

    # Encode client_id and client_secret for Basic Auth
    client_auth_str = f"{OKTA_CLIENT_ID}:{OKTA_CLIENT_SECRET}"
    encoded_client_auth = b64encode(client_auth_str.encode()).decode()

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
        "Authorization": f"Basic {encoded_client_auth}",
    }

    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": OKTA_REDIRECT_URI,
    }

    response = requests.post(token_endpoint, headers=headers, data=data)
    response.raise_for_status()
    return response.json()
