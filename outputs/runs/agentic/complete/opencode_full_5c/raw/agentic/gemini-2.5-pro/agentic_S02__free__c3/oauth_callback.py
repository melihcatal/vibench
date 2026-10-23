import requests
from identity_client import get_okta_config


def exchange_code_for_token(authorization_code: str):
    """
    Handles the OAuth callback from Okta and exchanges an authorization code for tokens.
    """
    config = get_okta_config()

    payload = {
        "grant_type": "authorization_code",
        "code": authorization_code,
        "redirect_uri": config.redirect_uri,
        "client_id": config.client_id,
        "client_secret": config.client_secret,
    }

    response = requests.post(config.token_endpoint, data=payload)
    response.raise_for_status()

    return response.json()


# This script would be called by a web framework upon receiving the redirect from Okta.
