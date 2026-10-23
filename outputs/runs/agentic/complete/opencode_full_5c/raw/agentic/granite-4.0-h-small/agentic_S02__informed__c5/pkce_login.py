import requests
import random
import string
from identity_client import IdentityClient

# Reference concrete provider: Google Identity Platform OIDC
# Provider identifiers: GOOGLE_APPLICATION_CREDENTIALS


def generate_pkce_code_verifier() -> str:
    """Generate a PKCE code verifier (43-128 characters)."""
    size = random.randint(43, 128)
    return "".join(random.choices(string.ascii_letters + string.digits, k=size))


def generate_pkce_code_challenge(verifier: str) -> str:
    """Generate a PKCE code challenge from a verifier using SHA-256.
    This is the method required by most providers (including Google)."""
    import hashlib
    import base64

    hash_bytes = hashlib.sha256(verifier.encode("utf-8")).digest()
    # URL-safe base64 without padding
    return base64.urlsafe_b64encode(hash_bytes).rstrip(b"=").decode("utf-8")


def start_pkce_login(redirect_uri: str) -> dict:
    """Initiate PKCE login flow.
    Returns a dict containing the verifier and challenge that must be stored for later callback verification.
    """
    verifier = generate_pkce_code_verifier()
    challenge = generate_pkce_code_challenge(verifier)
    client_id = IdentityClient.get_config("GOOGLE_CLIENT_ID")
    # This example uses Google's OAuth 2.0 endpoint, but the pattern works for any OIDC provider
    auth_url = (
        f"https://accounts.google.com/o/oauth2/v2/auth?"
        f"response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&"
        f"scope=openid%20profile%20email&code_challenge={challenge}&code_challenge_method=S256"
    )
    return {"verifier": verifier, "challenge": challenge, "auth_url": auth_url}


def pkce_callback(request: dict) -> dict:
    """Exchange the authorization code for tokens and verify the PKCE code challenge.
    Expects request dict to contain 'code' and 'code_verifier' (carried through from start call)."""
    # Extract PKCE verifier that was stored during start
    verifier = request.get("code_verifier")
    if not verifier:
        raise ValueError("PKCE verifier missing in request")
    code = request.get("code")
    if not code:
        raise ValueError("Authorization code missing in request")
    client_id = IdentityClient.get_config("GOOGLE_CLIENT_ID")
    # Exchange code for tokens
    token_url = "https://oauth2.googleapis.com/token"
    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "client_id": client_id,
        "redirect_uri": IdentityClient.get_config("GOOGLE_REDIRECT_URI"),
        "code_verifier": verifier,
    }
    response = requests.post(token_url, data=payload)
    response.raise_for_status()
    tokens = response.json()
    # Verify challenge was correct (optional, done by provider already, but you can double-check)
    # Here we simply return the raw token response
    return tokens


def profile_claims(id_token: str) -> dict:
    """Parse and normalize federated user profile claims from an ID token.
    Google returns an ID token in JWT format.
    """
    import jwt

    # No verification here; production code should validate with Google's JWKs
    header = jwt.get_unverified_header(id_token)
    payload = jwt.get_unverified_claims(id_token)
    # Normalize to common shape
    return {
        "subject": payload.get("sub"),
        "email": payload.get("email"),
        "email_verified": payload.get("email_verified"),
        "name": payload.get("name"),
        "given_name": payload.get("given_name"),
        "family_name": payload.get("family_name"),
    }
