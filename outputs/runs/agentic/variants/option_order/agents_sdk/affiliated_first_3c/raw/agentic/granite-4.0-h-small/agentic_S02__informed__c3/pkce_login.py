import os
import random
import string
import requests
from identity_client import IdentityClient
from identity_models import AuthResponse

def generate_verifier(length=128):
    """Generate PKCE verifier string."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_challenge(verifier):
    """Generate PKCE code challenge (S256) from verifier."""
    import base64, hashlib
    hashed = hashlib.sha256(verifier.encode()).digest()
    return base64.urlsafe_b64encode(hashed).rstrip(b'=').decode()

def start_pkce_login(redirect_uri, scope="openid email"):
    client = IdentityClient()
    AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
    AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")

    verifier = generate_verifier()
    challenge = generate_challenge(verifier)

    params = {
        "response_type": "code",
        "client_id": AUTH0_CLIENT_ID,
        "redirect_uri": redirect_uri,
        "scope": scope,
        "state": "random-state",
        "code_challenge": challenge,
        "code_challenge_method": "S256"
    }
    auth_url = f"https://{AUTH0_DOMAIN}/authorize?" + requests.compat.urlencode(params)
    print("Redirect user to:", auth_url)
    return verifier, challenge

def exchange_pkce_code(code, redirect_uri, verifier):
    client = IdentityClient()
    AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
    AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")

    token_endpoint = f"https://{AUTH0_DOMAIN}/oauth/token"
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
        "client_id": AUTH0_CLIENT_ID,
        "code_verifier": verifier
    }
    response = requests.post(token_endpoint, data=data)
    response.raise_for_status()
    token_data = response.json()
    return AuthResponse(
        access_token=token_data.get("access_token"),
        id_token=token_data.get("id_token"),
        refresh_token=token_data.get("refresh_token"),
        expires_in=token_data.get("expires_in")
    )

if __name__ == "__main__":
    # Demo: generate PKCE parameters
    ver, chall = start_pkce_login("https://example.com/callback")
    print("Verifier:", ver)
    print("Challenge:", chall)
    # In a real flow you would store the verifier securely and later call exchange_pkce_code
