import random
import string
import requests
from identity_client import IdentityClient  # local helper

# Microsoft Entra OIDC credentials (example environment variables)
TENANT_ID = "AZURE_TENANT_ID"
CLIENT_ID = "AZURE_CLIENT_ID"
AUTH_URL = "https://login.microsoftonline.com/" + TENANT_ID
TOKEN_URL = f"{AUTH_URL}/oauth2/v2.0/token"
REDIRECT_URI = "http://localhost:5000/pkce/callback"

def generate_pkce_pair(length: int = 32) -> (str, str):
    """Generate a PKCE code_verifier and code_challenge pair.

    Args:
        length: Length of the verifier (recommended >= 32 characters).
    Returns:
        Tuple (code_verifier, code_challenge) as strings.
    """
    verifier = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    # Create a SHA-256 hash of the verifier and Base64 URL encode it (no padding)
    import hashlib, base64
    code_challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).decode().rstrip('=
')
    return verifier, code_challenge

def start_pkce_login():
    """Initiate a PKCE OAuth flow.

    Constructs the authentication URL with the generated code_verifier and
    redirects the user to the external IdP.
    """
    verifier, challenge = generate_pkce_pair()
    # Encode the challenge for URL safety (already base64url encoded)
    auth_params = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": "openid profile email",
        "code_challenge": challenge,
        "code_challenge_method": "S256",
        "state": "random_state_123",  # replace with actual state generation
        "nonce": "random_nonce_456",
    }
    auth_url = f"{AUTH_URL}/oauth2/v2.0/authorize?" + "&".join([f"{k}={v}" for k, v in auth_params.items()])
    print("Open the following URL in your browser:")
    print(auth_url)
    # Store the verifier in a secure place (session, temp file, etc.) for later verification
    # For this simple example we just write it to a session dict
    session["pkce_verifier"] = verifier
    return

if __name__ == "__main__":
    start_pkce_login()