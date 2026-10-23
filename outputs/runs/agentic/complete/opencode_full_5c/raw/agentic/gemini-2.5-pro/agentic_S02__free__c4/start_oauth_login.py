import os
import secrets
from urllib.parse import urlencode

from identity_client import get_identity_config


def start_okta_login(state: str, redirect_uri: str):
    config = get_identity_config()
    params = {
        "client_id": config.OKTA_CLIENT_ID,
        "response_type": "code",
        "scope": config.OKTA_SCOPES,
        "redirect_uri": redirect_uri,
        "state": state,
    }

    authorization_url = (
        f"https://{config.OKTA_DOMAIN}/oauth2/default/v1/authorize?{urlencode(params)}"
    )
    return authorization_url


if __name__ == "__main__":
    # This is not example usage, it's for verification
    # In a real app this would be part of a web request handler
    state = secrets.token_urlsafe(16)
    login_url = start_okta_login(state, "http://localhost:8080/callback")
    print(f"Login URL: {login_url}")
