import os
import base64
import hashlib
import urllib.parse
from identity_client import AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_CALLBACK_URL

def generate_pkce_challenge():
    """Generates PKCE code_verifier and code_challenge."""
    code_verifier = base64.urlsafe_b64encode(os.urandom(32)).rstrip(b'=').decode('utf-8')
    
    # S256 code_challenge
    hashed = hashlib.sha256(code_verifier.encode('utf-8')).digest()
    code_challenge = base64.urlsafe_b64encode(hashed).rstrip(b'=').decode('utf-8')
    
    return code_verifier, code_challenge

def start_pkce_login():
    """Constructs and returns the Auth0 authorization URL for a PKCE flow."""
    code_verifier, code_challenge = generate_pkce_challenge()
    
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
    
    login_url = f"{authorize_url}?{urllib.parse.urlencode(params)}"
    return login_url, code_verifier

if __name__ == "__main__":
    login_url, code_verifier = start_pkce_login()
    print(f"Please visit this URL to start the PKCE login process: {login_url}")
    print(f"Your PKCE code_verifier (keep this secret!): {code_verifier}")
    print("You will need this code_verifier to exchange the authorization code for tokens.")
