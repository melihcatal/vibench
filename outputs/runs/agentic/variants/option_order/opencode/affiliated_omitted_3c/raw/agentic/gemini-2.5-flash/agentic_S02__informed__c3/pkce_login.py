import os
import base64
import hashlib
import secrets
import uuid
from typing import Tuple
from identity_client import Auth0Client


def generate_pkce_challenge() -> Tuple[str, str]:
    """Generates a PKCE code_verifier and code_challenge."""
    code_verifier = secrets.token_urlsafe(
        64
    )  # Generate a high-entropy cryptographically random string
    # S256 (SHA256) transformation
    s256_challenge = hashlib.sha256(code_verifier.encode("utf-8")).digest()
    code_challenge = (
        base64.urlsafe_b64encode(s256_challenge).decode("utf-8").replace("=", "")
    )
    return code_verifier, code_challenge


def start_pkce_login() -> Tuple[str, str]:
    """Starts a PKCE OAuth/OIDC login flow for public clients."""
    client = Auth0Client()
    state = str(uuid.uuid4())  # For CSRF protection
    code_verifier, code_challenge = generate_pkce_challenge()

    # In a real application, 'state' and 'code_verifier' would be stored in a session.

    auth_url = client.get_authorize_url(state=state, code_challenge=code_challenge)
    return auth_url, code_verifier


# Example usage (not part of the file, just for demonstration):
# if __name__ == "__main__":
#     os.environ["AUTH0_DOMAIN"] = "YOUR_AUTH0_DOMAIN.auth0.com"
#     os.environ["AUTH0_CLIENT_ID"] = "YOUR_AUTH0_CLIENT_ID"
#     os.environ["AUTH0_CALLBACK_URL"] = "http://localhost:8000/callback"
#     try:
#         auth_url, verifier = start_pkce_login()
#         print(f"Redirect to: {auth_url}")
#         print(f"Store this verifier for later: {verifier}")
#     except ValueError as e:
#         print(f"Configuration Error: {e}")
