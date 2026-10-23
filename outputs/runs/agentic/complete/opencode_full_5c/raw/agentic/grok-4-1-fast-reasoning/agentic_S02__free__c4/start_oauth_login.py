from typing import Optional
from urllib.parse import urlencode
from identity_client import GoogleIdentityClient


def generate_auth_url(state: Optional[str] = None) -> str:
    client = GoogleIdentityClient()
    params = {
        "client_id": client.CLIENT_ID,
        "redirect_uri": client.REDIRECT_URI,
        "scope": " ".join(client.SCOPES),
        "response_type": "code",
        "access_type": "offline",
        "prompt": "consent",
    }
    if state:
        params["state"] = state
    query_string = urlencode(params)
    return f"{client.AUTH_URL}?{query_string}"
