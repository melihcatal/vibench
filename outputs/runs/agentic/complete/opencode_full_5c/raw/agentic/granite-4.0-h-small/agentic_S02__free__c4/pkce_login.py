import secrets
import urllib.parse
from identity_client import IdentityClient
from identity_models import PKCEChallenge


def generate_pkce_pair():
    """Generate a PKCE code verifier and challenge (S256 method)."""
    verifier = secrets.token_urlsafe(32)
    # Compute SHA256 and base64url encode per RFC 7636
    import hashlib, base64

    verifier_bytes = verifier.encode("utf-8")
    hash_bytes = hashlib.sha256(verifier_bytes).digest()
    challenge = base64.urlsafe_b64encode(hash_bytes).rstrip(b"=").decode("utf-8")
    return verifier, challenge


def start_pkce_login(client_id, redirect_uri):
    """Start an authorization-code flow with PKCE for public clients.

    Uses Auth0 as the concrete external identity provider.
    Returns the authorization URL containing the code_challenge.
    """
    AUTH0_DOMAIN = "your-tenant.auth0.com"
    AUTH0_URL = f"https://{AUTH0_DOMAIN}/authorize"
    verifier, challenge = generate_pkce_pair()
    params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": "openid email profile",
        "code_challenge": challenge,
        "code_challenge_method": "S256",
    }
    url = f"{AUTH0_URL}?{urllib.parse.urlencode(params)}"
    return url, verifier


if __name__ == "__main__":
    client = IdentityClient()
    auth_url, code_verifier = start_pkce_login(client.client_id, client.redirect_uri)
    print("Redirect user to auth URL:", auth_url)
    # Store code_verifier securely for later verification after callback
    print("Store this code_verifier for callback verification:", code_verifier)
