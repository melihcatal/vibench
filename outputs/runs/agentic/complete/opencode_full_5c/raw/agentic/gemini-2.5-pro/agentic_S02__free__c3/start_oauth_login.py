import os
from urllib.parse import urlencode
from identity_client import get_okta_config


def start_okta_login():
    """
    Starts the OAuth 2.0 authorization code flow with Okta.
    """
    config = get_okta_config()
    params = {
        "client_id": config.client_id,
        "response_type": "code",
        "scope": config.scope,
        "redirect_uri": config.redirect_uri,
        "state": os.urandom(16).hex(),
    }

    authorization_url = f"{config.authorization_endpoint}?{urlencode(params)}"
    return authorization_url


# Example of an environment variable for Okta:
# export OKTA_DOMAIN="https://dev-123456.okta.com"
