import os
import base64
import hashlib
import random
import string
import urllib.parse

from identity_client import IdentityClient

# Provider: Cognito Hosted UI (OAuth2 with PKCE)
COGNITO_AUTH_URL = (
    "https://YOUR_COGNITO_DOMAIN.auth.us-east-1.amazoncognito.com/oauth2/authorize"
)


def pkce_login(
    client_id: str,
    redirect_uri: str,
    scopes: list[str] = None,
    state: str = None,
) -> str:
    """Generate an OAuth2 authorization URL using PKCE for public clients.

    Args:
        client_id: OAuth client ID (public).
        redirect_uri: Where the user is sent after consent.
        scopes: Optional list of OAuth scopes.
        state: Optional CSRF protection state token.

    Returns:
        Full authorization URL that the client can redirect to.
    """
    # Generate the PKCE verifier and code_challenge per RFC 7636
    verifier = IdentityClient.generate_pkce_verifier()
    challenge = IdentityClient.derive_pkce_challenge(verifier)
    params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "code_challenge": challenge,
        "code_challenge_method": "S256",
        "prompt": "login consent",
        "access_type": "offline",
    }
    if scopes:
        params["scope"] = " ".join(scopes)
    if state:
        params["state"] = state
    query = urllib.parse.urlencode(params)
    return COGNITO_AUTH_URL + "?" + query
