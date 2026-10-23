import os
import secrets
from urllib.parse import urlencode

from identity_client import get_auth0_authorize_url


def start_oauth_login(redirect_uri: str) -> str:
    """Starts an OAuth authorization-code login flow with Auth0.

    Args:
        redirect_uri: The URI to redirect to after successful authentication.

    Returns:
        The URL to redirect the user to for login.
    """
    state = secrets.token_urlsafe(16)
    # In a real application, you would store the state in a session
    # to verify it in the callback.
    # For this example, we'll just return the URL.

    auth_url = get_auth0_authorize_url(redirect_uri, state)
    return auth_url
