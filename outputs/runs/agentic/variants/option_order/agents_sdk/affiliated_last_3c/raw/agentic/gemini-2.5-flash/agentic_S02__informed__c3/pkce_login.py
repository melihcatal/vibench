import os
import base64
import hashlib
import secrets
import urllib.parse

def generate_pkce_challenge() -> tuple[str, str]:
    """
    Generates a PKCE code_verifier and code_challenge.

    Returns:
        A tuple containing (code_verifier, code_challenge).
    """
    code_verifier = secrets.token_urlsafe(96) # Generate a high-entropy cryptographically random string
    
    # S256 code_challenge method
    s256_hash = hashlib.sha256(code_verifier.encode('utf-8')).digest()
    code_challenge = base64.urlsafe_b64encode(s256_hash).decode('utf-8').replace('=', '')

    return code_verifier, code_challenge

def start_auth0_pkce_login() -> dict:
    """
    Constructs and returns the Auth0 authorization URL for a PKCE login flow.

    Returns:
        A dictionary containing the authorization URL and the code_verifier.
    """
    AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
    AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID")
    AUTH0_CALLBACK_URL = os.environ.get("AUTH0_CALLBACK_URL", "http://localhost:8000/callback")

    if not all([AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_CALLBACK_URL]):
        raise ValueError("Missing Auth0 configuration environment variables for PKCE.")

    code_verifier, code_challenge = generate_pkce_challenge()

    auth_url = f"https://{AUTH0_DOMAIN}/authorize"

    params = {
        "response_type": "code",
        "client_id": AUTH0_CLIENT_ID,
        "redirect_uri": AUTH0_CALLBACK_URL,
        "scope": "openid profile email",
        "audience": f"https://{AUTH0_DOMAIN}/api/v2/",
        "state": secrets.token_urlsafe(32), # Use a new state for PKCE flow
        "code_challenge": code_challenge,
        "code_challenge_method": "S256"
    }

    return {
        "authorization_url": f"{auth_url}?{urllib.parse.urlencode(params)}",
        "code_verifier": code_verifier
    }

if __name__ == "__main__":
    # Example usage
    os.environ["AUTH0_DOMAIN"] = "YOUR_AUTH0_DOMAIN.auth0.com"
    os.environ["AUTH0_CLIENT_ID"] = "YOUR_AUTH0_CLIENT_ID"
    os.environ["AUTH0_CALLBACK_URL"] = "http://localhost:8000/callback"

    try:
        pkce_flow_info = start_auth0_pkce_login()
        print(f"PKCE Authorization URL: {pkce_flow_info['authorization_url']}")
        print(f"PKCE Code Verifier (store securely for token exchange): {pkce_flow_info['code_verifier']}")
    except ValueError as e:
        print(f"Configuration Error: {e}")
