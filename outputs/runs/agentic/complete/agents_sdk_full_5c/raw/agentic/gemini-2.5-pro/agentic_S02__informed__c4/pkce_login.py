import os
import hashlib
import base64
from auth0.authentication import Authorize
from identity_client import get_auth0_config

def generate_pkce_challenge():
    """Generates a code verifier and its corresponding code challenge for PKCE."""
    code_verifier = base64.urlsafe_b64encode(os.urandom(40)).decode('utf-8')
    code_verifier = code_verifier.rstrip('=')

    code_challenge = hashlib.sha256(code_verifier.encode('utf-8')).digest()
    code_challenge = base64.urlsafe_b64encode(code_challenge).decode('utf-8')
    code_challenge = code_challenge.rstrip('=')

    return code_verifier, code_challenge

def start_pkce_flow(redirect_uri: str, state: str):
    """
    Generates an authorization URL for a PKCE flow.

    Args:
        redirect_uri: The callback URL.
        state: An opaque value for security.

    Returns:
        A tuple containing the authorization URL and the code verifier
        (which must be stored by the client to be used later).
    """
    config = get_auth0_config()
    auth0_authorize = Authorize(config["domain"])
    
    code_verifier, code_challenge = generate_pkce_challenge()

    auth_url = auth0_authorize.get_url(
        client_id=config["client_id"],
        audience="",
        state=state,
        redirect_uri=redirect_uri,
        response_type="code",
        scope="openid profile email",
        code_challenge=code_challenge,
        code_challenge_method="S256"
    )

    return auth_url, code_verifier

# To complete the flow, the `code_verifier` would be sent along with the
# authorization code to the token endpoint.
