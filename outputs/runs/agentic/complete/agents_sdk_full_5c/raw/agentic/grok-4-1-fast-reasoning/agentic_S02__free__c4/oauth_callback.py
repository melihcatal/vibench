import requests
from identity_client import GoogleOAuthConfig
from identity_models import OAuthToken

def oauth_callback(code: str):
    config = GoogleOAuthConfig()
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": config.REDIRECT_URI,
        "client_id": config.CLIENT_ID,
        "client_secret": config.CLIENT_SECRET,
    }
    response = requests.post(config.TOKEN_URL, data=data)
    response.raise_for_status()
    tokens = response.json()
    return OAuthToken(**tokens)