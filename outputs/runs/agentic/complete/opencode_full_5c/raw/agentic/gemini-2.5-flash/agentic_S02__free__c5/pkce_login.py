import os
import base64
import hashlib
import secrets
import urllib.parse


def generate_pkce_codes():
    """
    Generates PKCE code_verifier and code_challenge.
    """
    code_verifier = secrets.token_urlsafe(96)  # Generate a random string

    # Hash the code_verifier using SHA256
    hashed = hashlib.sha256(code_verifier.encode("utf-8")).digest()

    # Base64url-encode the hash
    code_challenge = base64.urlsafe_b64encode(hashed).decode("utf-8").replace("=", "")

    return code_verifier, code_challenge


def start_auth0_pkce_login():
    """
    Constructs the Auth0 authorization URL for a PKCE login flow.
    """
    AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN", "YOUR_AUTH0_DOMAIN.auth0.com")
    AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID", "YOUR_AUTH0_CLIENT_ID_FOR_PKCE")
    AUTH0_CALLBACK_URL = os.environ.get(
        "AUTH0_CALLBACK_URL", "http://localhost:8000/pkce-callback"
    )

    code_verifier, code_challenge = generate_pkce_codes()

    authorize_url = f"https://{AUTH0_DOMAIN}/authorize"
    params = {
        "response_type": "code",
        "client_id": AUTH0_CLIENT_ID,
        "redirect_uri": AUTH0_CALLBACK_URL,
        "scope": "openid profile email",
        "audience": f"https://{AUTH0_DOMAIN}/api/v2/",
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    }

    # In a real application, you would store the code_verifier securely for later use in the token exchange.
    print(f"PKCE Code Verifier (STORE THIS SECURELY): {code_verifier}")

    return f"{authorize_url}?{urllib.parse.urlencode(params)}"


if __name__ == "__main__":
    pkce_login_url = start_auth0_pkce_login()
    print(f"Please visit this URL for PKCE login: {pkce_login_url}")
