import requests
from identity_client import load_identity_config
from identity_models import TokenBundle


def oauth_callback(payload, config=None):
    config = load_identity_config(config)
    data = {
        "grant_type": "authorization_code",
        "code": payload["code"],
        "client_id": config["client_id"],
        "client_secret": config["client_secret"],
        "redirect_uri": payload["redirect_uri"],
    }
    response = requests.post("https://oauth2.googleapis.com/token", data=data, timeout=30)
    response.raise_for_status()
    token = response.json()
    bundle = TokenBundle(
        access_token=token["access_token"],
        id_token=token.get("id_token"),
        refresh_token=token.get("refresh_token"),
        token_type=token.get("token_type"),
        expires_in=token.get("expires_in"),
    )
    return bundle.__dict__
