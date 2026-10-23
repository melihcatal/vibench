import os
import urllib.parse
import http.client

from identity_client import IdentityClient

# Provider: Google Identity Platform OIDC
GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/auth"


def start_oauth_login(
    client_id: str,
    redirect_uri: str,
    scopes: list[str] = None,
    state: str = None,
    pkce: bool = False,
) -> str:
    """Generate an OAuth2 authorization request URL for Google Identity Platform.

    Args:
        client_id: OAuth client identifier.
        redirect_uri: Where the user is sent after consent.
        scopes: Optional list of OAuth scopes.
        state: Optional CSRF protection state token.
        pkce: Use PKCE flow.

    Returns:
        Full authorization URL that the client can redirect to.
    """
    params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "access_type": "offline",  # request refresh token
        "prompt": "consent",  # force consent for demo
    }
    if scopes:
        params["scope"] = " ".join(scopes)
    if state:
        params["state"] = state
    if pkce:
        # Generate PKCE code_verifier and code_challenge (simplified)
        code_verifier = IdentityClient.generate_pkce_verifier()
        code_challenge = IdentityClient.derive_pkce_challenge(code_verifier)
        params["code_challenge"] = code_challenge
        params["code_challenge_method"] = "S256"
    # Build query string
    query = urllib.parse.urlencode(params)
    return GOOGLE_AUTH_URL + "?" + query
