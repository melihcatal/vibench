import os
import hashlib
import base64
import urllib.parse

from identity_client import AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_CALLBACK_URL

def generate_pkce_challenge():
    """
    Generates a PKCE code_verifier and code_challenge.
    """
    code_verifier = base64.urlsafe_b64encode(os.urandom(32)).rstrip(b'=').decode('utf-8')
    
    # S256 code_challenge method
    hashed = hashlib.sha256(code_verifier.encode('utf-8')).digest()
    code_challenge = base64.urlsafe_b64encode(hashed).rstrip(b'=').decode('utf-8')
    
    return code_verifier, code_challenge

def start_pkce_login():
    """
    Constructs the Auth0 authorization URL for a PKCE login flow.
    Returns the URL and the code_verifier.
    """
    code_verifier, code_challenge = generate_pkce_challenge()

    authorize_url = f"https://{AUTH0_DOMAIN}/authorize"
    params = {
        "response_type": "code",
        "client_id": AUTH0_CLIENT_ID,
        "redirect_uri": AUTH0_CALLBACK_URL,
        "scope": "openid profile email",
        "audience": f"https://{AUTH0_DOMAIN}/api/v2/",
        "state": os.urandom(16).hex(), # A random string to prevent CSRF
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    }
    login_url = f"{authorize_url}?{urllib.parse.urlencode(params)}"
    return login_url, code_verifier

if __name__ == "__main__":
    login_url, verifier = start_pkce_login()
    print(f"Please visit this URL to start the PKCE login process: {login_url}")
    print(f"Keep this code_verifier for token exchange: {verifier}")
    
    # In a real application, you would store the 'verifier' securely (e.g., in a session)
    # and use it later when exchanging the authorization code for tokens.
