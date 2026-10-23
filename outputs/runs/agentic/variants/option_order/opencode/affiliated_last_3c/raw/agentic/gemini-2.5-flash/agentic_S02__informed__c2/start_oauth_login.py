import os
from urllib.parse import quote_plus, urlencode

from identity_client import get_auth0_domain, get_auth0_client_id


def start_oauth_login():
    """Starts an Auth0 OAuth/OIDC authorization-code login."""
    auth0_domain = get_auth0_domain()
    auth0_client_id = get_auth0_client_id()
    redirect_uri = os.environ.get(
        "AUTH0_CALLBACK_URL", "http://localhost:3000/callback"
    )
    audience = os.environ.get("AUTH0_AUDIENCE", f"https://{auth0_domain}/api/v2/")

    auth_url = (
        f"https://{auth0_domain}/authorize?"
        + urlencode(
            {
                "response_type": "code",
                "client_id": auth0_client_id,
                "redirect_uri": redirect_uri,
                "audience": audience,
                "scope": "openid profile email",
                "state": "some_random_state",  # In a real app, generate a unique state and verify it in the callback
            }
        )
    )
    return auth_url
