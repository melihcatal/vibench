from identity_client import GOOGLE_TOKEN_URL, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET
from identity_models import OAuth2TokenResponse


def oauth_callback(code: str):
    token_url = GOOGLE_TOKEN_URL
    data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": "http://localhost:8000/oauth_callback",
        "grant_type": "authorization_code",
    }
    response = requests.post(token_url, data=data)
    response.raise_for_status()
    token_data = response.json()
    return OAuth2TokenResponse.from_dict(token_data)
