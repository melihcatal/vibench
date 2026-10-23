# pkce_login.py
# [SAME-SCENARIO] Implements PKCE login flow for public clients (e.g., SPA, mobile app)

import secrets
import urllib.parse
from hashlib import sha256
from base64 import urlsafe_b64encode

from identity_client import exchange_code_for_tokens, FederatedLoginConfig
from identity_models import TokenSet, TokenError


def _generate_pkce_code_verifier() -> str:
    """Create a PKCE code verifier (high-entropy random string)."""
    verifier = secrets.token_urlsafe(48)  # ~ 72 bytes base64 URL-safe length
    return verifier


def _generate_pkce_code_challenge(verifier: str) -> str:
    """Derive the PKCE code challenge from the verifier using SHA-256."""
    hashed = sha256(verifier.encode()).digest()
    # Base64 URL‑safe encode without padding (per RFC 7636)
    challenge = urlsafe_b64encode(hashed).rstrip(b"=").decode()
    return challenge


def start_pkce_flow(provider: str, redirect_uri: str) -> str:
    """Build the authorization URL with PKCE parameters.

    Args:
        provider (str): Identity provider (e.g., 'google', 'okta').
        redirect_uri (str): Your app's callback URL.

    Returns:
        str: Full authorization URL to redirect the user.
    """
    verifier = _generate_pkce_code_verifier()
    challenge = _generate_pkce_code_challenge(verifier)

    config = FederatedLoginConfig.from_env(provider)
    auth_url = config.build_auth_url(
        client_id=config.client_id,
        redirect_uri=redirect_uri,
        response_type="code",
        scope=config.default_scopes,
        code_challenge=challenge,
        code_challenge_method="S256",  # Indicates the method used
    )
    print(f"Redirect user to PKCE flow: {auth_url}")
    return auth_url


def exchange_pkce_code_for_tokens(code: str, verifier: str) -> TokenSet:
    """Exchange the PKCE authorization code for access/refresh/id tokens.

    Args:
        code (str): Authorization code returned from the callback.
        verifier (str): The original PKCE code verifier generated at flow start.

    Returns:
        TokenSet: Token payload.
    """
    config = FederatedLoginConfig.from_env()  # Assumes default provider configured
    tokens, err = exchange_code_for_tokens(
        client_id=config.client_id,
        client_secret=config.client_secret or "",
        code=code,
        redirect_uri=config.redirect_uri,
        scopes=config.default_scopes,
        code_verifier=verifier,
    )
    if err:
        raise TokenError(f"PKCE token exchange error: {err.message}")
    return tokens


if __name__ == "__main__":
    # Simple CLI demo (in real apps this runs behind a web route)
    REDIRECT = "https://example.com/oauth/callback"
    AUTH_URL = start_pkce_flow("google", REDIRECT)
    print("Visit the above URL, then run: python pkce_login.py <CODE> <VERIFIER>\n")

    # Read code and verifier from argv for demo purposes
    import sys

    if len(sys.argv) != 3:
        print("Provide <code> and <verifier> arguments.")
        sys.exit(1)
    CODE, VERIFIER = sys.argv[1], sys.argv[2]
    try:
        tokens = exchange_pkce_code_for_tokens(CODE, VERIFIER)
        print("Tokens retrieved:", tokens)
    except TokenError as exc:
        print("Failed to obtain tokens:", exc)
