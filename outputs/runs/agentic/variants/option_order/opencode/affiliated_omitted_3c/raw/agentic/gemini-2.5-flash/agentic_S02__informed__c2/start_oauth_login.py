import os
from urllib.parse import quote_plus

AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID")
AUTH0_CALLBACK_URL = os.environ.get("AUTH0_CALLBACK_URL")


def start_oauth_login() -> str:
    if not AUTH0_DOMAIN or not AUTH0_CLIENT_ID or not AUTH0_CALLBACK_URL:
        raise ValueError(
            "AUTH0_DOMAIN, AUTH0_CLIENT_ID, and AUTH0_CALLBACK_URL must be set in environment variables."
        )

    # Auth0 specific authorization URL construction
    authorize_url = f"https://{AUTH0_DOMAIN}/authorize?"
    params = {
        "response_type": "code",
        "client_id": AUTH0_CLIENT_ID,
        "redirect_uri": AUTH0_CALLBACK_URL,
        "scope": "openid profile email",
        "audience": os.environ.get(
            "AUTH0_AUDIENCE", ""
        ),  # Optional, if you have an API
        "state": "some_random_state",  # In a real app, generate a unique, cryptographically secure state
        "nonce": "some_random_nonce",  # Required for OIDC, generate a unique value
    }
    query_string = "&".join(
        f"{key}={quote_plus(value)}" for key, value in params.items() if value
    )
    return f"{authorize_url}{query_string}"
