import os
import secrets
import urllib.parse
from identity_client import IdentityClient


def start_oauth_login(redirect_uri, state=None, nonce=None):
    """Start OAuth/OIDC authorization code login flow."""
    client = IdentityClient()

    # Generate state and nonce if not provided
    if state is None:
        state = secrets.token_urlsafe(16)
    if nonce is None:
        nonce = secrets.token_urlsafe(16)

    # Auth0 specific OIDC configuration
    auth0_domain = os.environ.get("AUTH0_DOMAIN")
    auth0_client_id = os.environ.get("AUTH0_CLIENT_ID")

    if not auth0_domain or not auth0_client_id:
        raise ValueError(
            "AUTH0_DOMAIN and AUTH0_CLIENT_ID environment variables must be set"
        )

    # Build Auth0 authorization URL
    auth_params = {
        "response_type": "code",
        "client_id": auth0_client_id,
        "redirect_uri": redirect_uri,
        "scope": "openid profile email",
        "state": state,
        "nonce": nonce,
    }

    auth_url = f"https://{auth0_domain}/authorize?{urllib.parse.urlencode(auth_params)}"

    # Store state and nonce for validation in callback
    client.store_auth_state(state, nonce, redirect_uri)

    return {"auth_url": auth_url, "state": state, "nonce": nonce}
