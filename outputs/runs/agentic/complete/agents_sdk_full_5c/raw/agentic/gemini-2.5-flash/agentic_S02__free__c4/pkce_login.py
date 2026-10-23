import os
import base64
import hashlib
import secrets
from urllib.parse import urlencode
import requests

# Okta OAuth 2.0 with PKCE
OKTA_ORG_URL = os.environ.get("OKTA_ORG_URL", "https://{your-okta-domain}.okta.com")
OKTA_CLIENT_ID = os.environ.get("OKTA_CLIENT_ID", "YOUR_OKTA_CLIENT_ID")
OKTA_REDIRECT_URI = os.environ.get("OKTA_REDIRECT_URI", "http://localhost:8080/pkce/callback")
OKTA_AUTHZ_SERVER_ID = os.environ.get("OKTA_AUTHZ_SERVER_ID", "default") # or 'default'

# Helper function for PKCE
def generate_pkce_codes():
    code_verifier = secrets.token_urlsafe(64) # Generate a high-entropy cryptographically random string
    # S256 (SHA256) code_challenge_method
    s256 = hashlib.sha256(code_verifier.encode('utf-8')).digest()
    code_challenge = base64.urlsafe_b64encode(s256).decode('utf-8').replace('=', '')
    return code_verifier, code_challenge

def get_okta_pkce_auth_url():
    code_verifier, code_challenge = generate_pkce_codes()
    
    # Store code_verifier securely in session for later use during token exchange
    # In a real app, this would be stored in the user's session.
    print(f"DEBUG: Store this code_verifier securely for callback: {code_verifier}")

    params = {
        "client_id": OKTA_CLIENT_ID,
        "redirect_uri": OKTA_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid profile email",
        "code_challenge_method": "S256",
        "code_challenge": code_challenge,
    }
    auth_url = f"{OKTA_ORG_URL}/oauth2/{OKTA_AUTHZ_SERVER_ID}/v1/authorize?{urlencode(params)}"
    return auth_url, code_verifier # Returning code_verifier for demonstration/testing

def exchange_pkce_code_for_tokens(auth_code: str, code_verifier: str):
    token_url = f"{OKTA_ORG_URL}/oauth2/{OKTA_AUTHZ_SERVER_ID}/v1/token"
    token_params = {
        "grant_type": "authorization_code",
        "client_id": OKTA_CLIENT_ID,
        "redirect_uri": OKTA_REDIRECT_URI,
        "code": auth_code,
        "code_verifier": code_verifier,
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(token_url, data=token_params, headers=headers)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    auth_url, verifier = get_okta_pkce_auth_url()
    print(f"Navigate to this URL to start Okta PKCE login: {auth_url}")
    print(f"Remember to use the verifier '{verifier}' in the callback step.")
    
    # Example of callback (in a real app, this would be a separate handler)
    # Simulating a callback with a dummy code and the stored verifier
    # Replace with a real authorization code from Okta after login
    # example_auth_code = "YOUR_OKTA_AUTH_CODE_FROM_CALLBACK"
    # 
    # if example_auth_code != "YOUR_OKTA_AUTH_CODE_FROM_CALLBACK":
    #     try:
    #         tokens = exchange_pkce_code_for_tokens(example_auth_code, verifier)
    #         import json
    #         print("\nSuccessfully exchanged PKCE code for tokens:")
    #         print(json.dumps(tokens, indent=2))
    #     except requests.exceptions.HTTPError as e:
    #         print(f"Error during token exchange: {e.response.text}")
    #     except Exception as e:
    #         print(f"An unexpected error occurred: {e}")
    # else:
    #     print("\nSkipping token exchange example: please replace 'YOUR_OKTA_AUTH_CODE_FROM_CALLBACK' with a real code.")
