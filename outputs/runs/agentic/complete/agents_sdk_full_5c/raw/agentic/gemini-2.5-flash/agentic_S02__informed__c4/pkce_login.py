import os
import urllib.parse
import hashlib
import base64
import secrets
import requests
import json

AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID")
AUTH0_CALLBACK_URL = os.environ.get("AUTH0_CALLBACK_URL")

def generate_pkce_challenge():
    """Generates PKCE code_verifier and code_challenge."""
    code_verifier = secrets.token_urlsafe(64)
    s256 = hashlib.sha256(code_verifier.encode("utf-8")).digest()
    code_challenge = base64.urlsafe_b64encode(s256).decode("utf-8").replace("=", "")
    return code_verifier, code_challenge

def start_auth0_pkce_login():
    """Starts an Auth0 PKCE OAuth 2.0 Authorization Code Grant flow."""
    if not all([AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_CALLBACK_URL]):
        raise ValueError("Missing Auth0 environment variables.")
    
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
    # In a real application, you'd store the code_verifier securely (e.g., in a session)
    # and retrieve it during the callback to exchange the code.
    print(f"PKCE Code Verifier (store securely): {code_verifier}")
    return f"{authorize_url}?{urllib.parse.urlencode(params)}", code_verifier

def exchange_auth0_pkce_code_for_tokens(auth_code: str, code_verifier: str):
    """Exchanges the authorization code for tokens using PKCE code_verifier."""
    if not all([AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_CALLBACK_URL]):
        raise ValueError("Missing Auth0 environment variables.")

    token_url = f"https://{AUTH0_DOMAIN}/oauth/token"
    headers = {'Content-Type': 'application/json'}
    payload = {
        'grant_type': 'authorization_code',
        'client_id': AUTH0_CLIENT_ID,
        'code': auth_code,
        'redirect_uri': AUTH0_CALLBACK_URL,
        'code_verifier': code_verifier
    }

    try:
        response = requests.post(token_url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error exchanging PKCE code for tokens: {e}")
        return None

if __name__ == "__main__":
    login_url, verifier = start_auth0_pkce_login()
    print(f"Redirect for PKCE login: {login_url}")
    # Simulate callback with an authorization code and stored verifier
    # In a real app, 'auth_code' would come from the URL and 'verifier' from session storage.
    # simulated_auth_code = "YOUR_SIMULATED_AUTH_CODE"
    # tokens = exchange_auth0_pkce_code_for_tokens(simulated_auth_code, verifier)
    # if tokens:
    #     print("PKCE tokens received:")
    #     print(json.dumps(tokens, indent=2))
