import requests
from typing import Optional
from identity_client import GoogleIdentityClient
from identity_models import TokenResponse


def exchange_auth_code(code: str, state: Optional[str] = None) -> TokenResponse:
    client = GoogleIdentityClient()
    data = {
        "client_id": client.CLIENT_ID,
        "client_secret": client.CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": client.REDIRECT_URI,
    }
    response = requests.post(client.TOKEN_URL, data=data)
    response.raise_for_status()
    tokens = response.json()
    return TokenResponse(**tokens)
