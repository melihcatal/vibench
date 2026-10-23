import os
from urllib.parse import urlencode
from identity_client import get_auth0_config


def start_oauth_login() -> str:
    config = get_auth0_config()
    if not config.domain or not config.client_id or not config.redirect_uri:
        raise ValueError("Auth0 domain, client ID, or redirect URI not configured.")

    authorize_url = f"https://{config.domain}/authorize"
    params = {
        "client_id": config.client_id,
        "response_type": "code",
        "redirect_uri": config.redirect_uri,
        "scope": "openid profile email",
        "audience": os.environ.get(
            "AUTH0_AUDIENCE"
        ),  # Optional, depending on API access
    }
    return f"{authorize_url}?{urlencode(params)}"
