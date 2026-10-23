import requests
from urllib.parse import parse_qs
from identity_client import TOKEN_URL, AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET, REDIRECT_URI
from identity_models import OauthToken

def handle_callback(query_string: str) -> OauthToken:
    params = parse_qs(query_string)
    code = params.get('code', [None])[0]
    if not code:
        raise ValueError("No authorization code in callback")
    data = {
        "grant_type": "authorization_code",
        "client_id": AUTH0_CLIENT_ID,
        "client_secret": AUTH0_CLIENT_SECRET,
        "code": code,
        "redirect_uri": REDIRECT_URI,
    }
    resp = requests.post(TOKEN_URL, data=data)
    resp.raise_for_status()
    token_data = resp.json()
    return OauthToken(
        access_token=token_data["access_token"],
        token_type=token_data["token_type"],
        id_token=token_data.get("id_token"),
        refresh_token=token_data.get("refresh_token"),
    )