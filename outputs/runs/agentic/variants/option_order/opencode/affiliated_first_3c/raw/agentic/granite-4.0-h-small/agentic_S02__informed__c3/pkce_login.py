import os
import secrets
import requests
from identity_client import IdentityClient

# IBM App ID Federation configuration
APP_ID_CLIENT_ID = os.getenv("IBM_APPID_CLIENT_ID")
REDIRECT_URI = os.getenv("REDIRECT_URI", "http://localhost:8000/oauth_callback")


def generate_pkce_pair(length=128):
    """Generate a PKCE code_verifier and the corresponding code_challenge."""
    verifier = secrets.token_urlsafe(length)
    import hashlib

    challenge = hashlib.sha256(verifier.encode()).digest()
    challenge_b64 = requests.utils.quote(
        base64.urlsafe_b64encode(challenge).decode().rstrip("=")
    )
    return verifier, challenge_b64


def start_pkce_login():
    """Initiate a PKCE-enabled authorization-code login with IBM App ID."""
    verifier, challenge = generate_pkce_pair()
    client = IdentityClient(
        client_id=APP_ID_CLIENT_ID,
        redirect_uri=REDIRECT_URI,
        issuer="https://iam.cloud.ibm.com/identity",
    )
    state = client.generate_state()
    # Build authorization URL with PKCE parameters
    auth_url = (
        f"{client.issuer}/op/authorize?"
        f"response_type=code&"
        f"client_id={client.client_id}&"
        f"redirect_uri={requests.utils.quote(REDIRECT_URI)}&"
        f"scope=openid%20profile%20email&"
        f"state={state}&"
        f"code_challenge={challenge}&"
        f"code_challenge_method=S256"
    )
    print("Redirect user to:")
    print(auth_url)
    print("Store code_verifier securely for later token exchange")
    return verifier


# Example mock storage placeholder
if __name__ == "__main__":
    # In real app store the verifier in a secure server-side session
    stored_verifier = start_pkce_login()
    # Simulate saving to session/store
    print("Store this verifier for later use:", stored_verifier)
