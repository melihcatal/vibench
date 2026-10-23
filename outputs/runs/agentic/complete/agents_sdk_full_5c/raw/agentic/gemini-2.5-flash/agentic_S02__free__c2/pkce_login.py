import os
import base64
import hashlib
import secrets
import urllib.parse
import requests
import json

# Okta PKCE Login Flow
OKTA_ORG_URL = os.environ.get("OKTA_ORG_URL", "https://{your-okta-domain}.okta.com")
OKTA_CLIENT_ID = os.environ.get("OKTA_CLIENT_ID", "YOUR_OKTA_CLIENT_ID")
OKTA_REDIRECT_URI = os.environ.get("OKTA_REDIRECT_URI", "http://localhost:8000/okta_callback")

OKTA_AUTHORIZE_URL = f"{OKTA_ORG_URL}/oauth2/default/v1/authorize"
OKTA_TOKEN_URL = f"{OKTA_ORG_URL}/oauth2/default/v1/token"

def generate_pkce_challenge():
    code_verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).rstrip(b'=').decode('utf-8')
    # S256 code challenge method
    code_challenge = base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode('utf-8')).digest()).rstrip(b'=').decode('utf-8')
    return code_verifier, code_challenge

def generate_okta_auth_url(code_challenge: str) -> str:
    params = {
        "client_id": OKTA_CLIENT_ID,
        "redirect_uri": OKTA_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid profile email",
        "code_challenge_method": "S256",
        "code_challenge": code_challenge,
    }
    return f"{OKTA_AUTHORIZE_URL}?{urllib.parse.urlencode(params)}"

def exchange_code_for_tokens_pkce(auth_code: str, code_verifier: str) -> dict:
    data = {
        "grant_type": "authorization_code",
        "client_id": OKTA_CLIENT_ID,
        "redirect_uri": OKTA_REDIRECT_URI,
        "code": auth_code,
        "code_verifier": code_verifier,
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    try:
        response = requests.post(OKTA_TOKEN_URL, data=data, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error exchanging code for Okta tokens: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    code_verifier, code_challenge = generate_pkce_challenge()
    print(f"Generated Code Verifier: {code_verifier}")
    print(f"Generated Code Challenge: {code_challenge}")

    auth_url = generate_okta_auth_url(code_challenge)
    print(f"\nVisit this URL to start Okta PKCE login:\n{auth_url}")

    # In a real application, you would store code_verifier in the session
    # and retrieve it during the callback to exchange the authorization code.
    print("\n(Remember to save the code_verifier for the callback step.)")
