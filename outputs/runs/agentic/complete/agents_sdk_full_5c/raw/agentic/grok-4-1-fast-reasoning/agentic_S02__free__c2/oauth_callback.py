import requests
from identity_client import get_client_config
from identity_models import TokenResponse

GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"

def oauth_callback(code: str, state: str, redirect_uri: str) -> TokenResponse:
    config = get_client_config("google")
    data = {
        "code": code,
        "client_id": config["client_id"],
        "client_secret": config["client_secret"],
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
    }
    response = requests.post(GOOGLE_TOKEN_URL, data=data)
    response.raise_for_status()
    tokens = TokenResponse.model_validate(response.json())
    return tokens