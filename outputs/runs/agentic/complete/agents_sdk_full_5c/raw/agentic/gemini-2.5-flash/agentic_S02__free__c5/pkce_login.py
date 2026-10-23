import os
import base64
import hashlib
import secrets
import urllib.parse

# Replace with your Auth0 domain and client ID
AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN", "YOUR_AUTH0_DOMAIN.auth0.com")
AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID", "YOUR_AUTH0_CLIENT_ID")
AUTH0_REDIRECT_URI = os.environ.get("AUTH0_REDIRECT_URI", "http://localhost:8000/auth0_callback")
AUTH0_SCOPE = "openid profile email"

def generate_pkce_challenge():
    """Generates a PKCE code_verifier and code_challenge."""
    code_verifier = secrets.token_urlsafe(64) # Generate a high-entropy cryptographically random string

    # Hash the code_verifier using SHA256
    hashed = hashlib.sha256(code_verifier.encode('utf-8')).digest()

    # Base64-URL-encode the hash
    code_challenge = base64.urlsafe_b64encode(hashed).decode('utf-8').replace('=', '')

    return code_verifier, code_challenge

def generate_auth0_pkce_url(code_challenge: str):
    """Generates the Auth0 authorization URL with PKCE parameters."""
    params = {
        "client_id": AUTH0_CLIENT_ID,
        "redirect_uri": AUTH0_REDIRECT_URI,
        "response_type": "code",
        "scope": AUTH0_SCOPE,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    }
    query_string = urllib.parse.urlencode(params)
    return f"https://{AUTH0_DOMAIN}/authorize?{query_string}"

if __name__ == "__main__":
    if "YOUR_AUTH0_DOMAIN" in AUTH0_DOMAIN or "YOUR_AUTH0_CLIENT_ID" in AUTH0_CLIENT_ID:
        print("Please set AUTH0_DOMAIN and AUTH0_CLIENT_ID environment variables or replace placeholders.")
    else:
        code_verifier, code_challenge = generate_pkce_challenge()
        print(f"Generated Code Verifier: {code_verifier}")
        print(f"Generated Code Challenge: {code_challenge}")

        auth_url = generate_auth0_pkce_url(code_challenge)
        print(f"\nPlease visit this URL to start the Auth0 PKCE login flow:\n{auth_url}")

        # In a real application, you would store the code_verifier securely in the user's session
        # and retrieve it during the token exchange step.
