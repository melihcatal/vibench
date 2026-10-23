import os
import base64
import hashlib
import secrets
import urllib.parse
import requests
import json

# Okta Configuration for PKCE flow
OKTA_ORG_URL = os.environ.get("OKTA_ORG_URL") # e.g., https://{your-okta-domain}.okta.com
OKTA_CLIENT_ID = os.environ.get("OKTA_CLIENT_ID")
OKTA_REDIRECT_URI = os.environ.get("OKTA_REDIRECT_URI")

def generate_pkce_codes():
    """
    Generates PKCE code_verifier and code_challenge.
    """
    code_verifier = secrets.token_urlsafe(64) # Generate a high-entropy cryptographically random string
    s256 = hashlib.sha256(code_verifier.encode('utf-8')).digest()
    code_challenge = base64.urlsafe_b64encode(s256).decode('utf-8').replace('=', '')
    return code_verifier, code_challenge

def start_okta_pkce_login():
    """
    Constructs the authorization URL for Okta using PKCE.
    """
    if not all([OKTA_ORG_URL, OKTA_CLIENT_ID, OKTA_REDIRECT_URI]):
        raise ValueError("Missing Okta configuration environment variables.")

    code_verifier, code_challenge = generate_pkce_codes()

    authorize_url = f"{OKTA_ORG_URL}/oauth2/default/v1/authorize" # Using default authorization server
    params = {
        "client_id": OKTA_CLIENT_ID,
        "response_type": "code",
        "scope": "openid profile email",
        "redirect_uri": OKTA_REDIRECT_URI,
        "state": secrets.token_urlsafe(16), # Random state for CSRF protection
        "code_challenge_method": "S256",
        "code_challenge": code_challenge,
    }
    query_string = urllib.parse.urlencode(params)
    authorization_url = f"{authorize_url}?{query_string}"

    # In a real application, you would store code_verifier and state securely in the user's session
    # to be used in the token exchange step.
    return authorization_url, code_verifier

def exchange_okta_pkce_code_for_tokens(authorization_code: str, code_verifier: str):
    """
    Exchanges the authorization code for tokens using PKCE code_verifier.
    """
    if not all([OKTA_ORG_URL, OKTA_CLIENT_ID, OKTA_REDIRECT_URI]):
        raise ValueError("Missing Okta configuration environment variables.")

    token_url = f"{OKTA_ORG_URL}/oauth2/default/v1/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    payload = {
        "grant_type": "authorization_code",
        "client_id": OKTA_CLIENT_ID,
        "redirect_uri": OKTA_REDIRECT_URI,
        "code": authorization_code,
        "code_verifier": code_verifier,
    }

    try:
        response = requests.post(token_url, headers=headers, data=payload)
        response.raise_for_status() # Raise an exception for HTTP errors
        tokens = response.json()
        return tokens
    except requests.exceptions.RequestException as e:
        print(f"Error exchanging code for tokens (Okta PKCE): {e}")
        return None

if __name__ == "__main__":
    # Example usage
    # auth_url, verifier = start_okta_pkce_login()
    # print(f"Okta PKCE Authorization URL: {auth_url}")
    # print(f"Store this code_verifier securely: {verifier}")

    # To test the exchange, you would need an actual authorization_code received
    # after the user completes the login in their browser.
    # sample_auth_code = "YOUR_RECEIVED_AUTH_CODE_HERE"
    # sample_code_verifier = verifier # Use the stored verifier

    # tokens = exchange_okta_pkce_code_for_tokens(sample_auth_code, sample_code_verifier)
    # if tokens:
    #     print("\nReceived Tokens:")
    #     print(json.dumps(tokens, indent=2))
    # else:
    #     print("Failed to get tokens.")
    print("To test, set environment variables and follow the PKCE flow manually.")
