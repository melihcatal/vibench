import requests

from identity_client import GOOGLE_TOKEN_ENDPOINT, load_identity_config
from identity_models import OAuthTokenResponse


def oauth_callback(code: str) -> OAuthTokenResponse:
    config = load_identity_config()
    response = requests.post(
        GOOGLE_TOKEN_ENDPOINT,
        data={
            "code": code,
            "client_id": config["google_client_id"],
            "client_secret": config["google_client_secret"],
            "redirect_uri": config["google_redirect_uri"],
            "grant_type": "authorization_code",
        },
        timeout=20,
    )
    response.raise_for_status()
    payload = response.json()
    return OAuthTokenResponse(
        access_token=payload["access_token"],
        id_token=payload.get("id_token"),
        refresh_token=payload.get("refresh_token"),
        token_type=payload.get("token_type", "Bearer"),
        expires_in=payload.get("expires_in"),
        raw=payload,
    )
