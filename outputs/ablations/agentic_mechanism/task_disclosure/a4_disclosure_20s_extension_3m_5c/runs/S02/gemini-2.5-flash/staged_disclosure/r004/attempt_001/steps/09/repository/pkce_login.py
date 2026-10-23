
import os
import base64
import hashlib
import json
import webbrowser
from urllib.parse import urlencode, urlparse, parse_qsl
import requests

# Auth0 specific details (replace with your actual Auth0 tenant details)
AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN", "YOUR_AUTH0_DOMAIN.auth0.com")
AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID", "YOUR_AUTH0_CLIENT_ID")
AUTH0_CALLBACK_URL = os.environ.get("AUTH0_CALLBACK_URL", "http://localhost:8080/callback")
AUTH0_AUDIENCE = os.environ.get("AUTH0_AUDIENCE", f"https://{AUTH0_DOMAIN}/api/v2/")

# --- PKCE Helper Functions ---
def generate_random_string(length=32):
    return base64.urlsafe_b64encode(os.urandom(length)).rstrip(b'=').decode('utf-8')

def sha256_challenge(code_verifier):
    s256 = hashlib.sha256(code_verifier.encode('utf-8')).digest()
    return base64.urlsafe_b64encode(s256).rstrip(b'=').decode('utf-8')

# --- PKCE Login Flow ---
def start_pkce_flow():
    code_verifier = generate_random_string(96)
    code_challenge = sha256_challenge(code_verifier)

    authorize_url = f"https://{AUTH0_DOMAIN}/authorize?" + urlencode({
        "response_type": "code",
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
        "client_id": AUTH0_CLIENT_ID,
        "redirect_uri": AUTH0_CALLBACK_URL,
        "scope": "openid profile email",
        "audience": AUTH0_AUDIENCE
    })

    print(f"Opening browser to: {authorize_url}")
    webbrowser.open(authorize_url)

    # In a real application, you would run a local web server here
    # to catch the redirect to AUTH0_CALLBACK_URL and extract the 'code'.
    # For this example, we'll simulate the next step after manual user intervention.
    print("\n-----")
    print("Please complete the login in your browser.")
    print(f"After successful login, your browser will be redirected to '{AUTH0_CALLBACK_URL}'.")
    print("Copy the 'code' query parameter from the redirected URL and paste it here.")
    auth_code = input("Enter the authorization code: ")

    return auth_code, code_verifier

def exchange_code_for_tokens(auth_code, code_verifier):
    token_url = f"https://{AUTH0_DOMAIN}/oauth/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    payload = {
        "grant_type": "authorization_code",
        "client_id": AUTH0_CLIENT_ID,
        "code_verifier": code_verifier,
        "code": auth_code,
        "redirect_uri": AUTH0_CALLBACK_URL,
        "audience": AUTH0_AUDIENCE
    }

    print(f"Exchanging code for tokens at: {token_url}")
    response = requests.post(token_url, headers=headers, data=payload)
    response.raise_for_status()
    return response.json()

def main():
    print("--- Starting Auth0 PKCE Login Flow ---")
    auth_code, code_verifier = start_pkce_flow()

    if auth_code:
        try:
            tokens = exchange_code_for_tokens(auth_code, code_verifier)
            print("\n--- Tokens Received ---")
            print(json.dumps(tokens, indent=2))

            # You can now use the access_token to call your API
            # For example:
            # access_token = tokens.get("access_token")
            # userinfo_url = f"https://{AUTH0_DOMAIN}/userinfo"
            # userinfo_response = requests.get(userinfo_url, headers={"Authorization": f"Bearer {access_token}"})
            # userinfo_response.raise_for_status()
            # print("\n--- User Info ---")
            # print(json.dumps(userinfo_response.json(), indent=2))

        except requests.exceptions.HTTPError as e:
            print(f"Error exchanging code for tokens: {e}")
            if e.response:
                print(e.response.text)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
    else:
        print("Authorization code not received. Aborting.")

if __name__ == "__main__":
    main()
