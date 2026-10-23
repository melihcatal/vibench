import base64
import hashlib
import os
import requests
import json

# Auth0 Domain and Client ID - REPLACE WITH YOUR OWN
AUTH0_DOMAIN = "YOUR_AUTH0_DOMAIN.auth0.com" # e.g., dev-yourcompany.auth0.com
AUTH0_CLIENT_ID = "YOUR_AUTH0_CLIENT_ID"
AUTH0_CALLBACK_URL = "http://localhost:8080/callback" # Must match your Auth0 application settings

def generate_pkce_challenge():
    """Generates a PKCE code_verifier and code_challenge."""
    code_verifier = base64.urlsafe_b64encode(os.urandom(32)).rstrip(b"=")
    hashed = hashlib.sha256(code_verifier).digest()
    code_challenge = base64.urlsafe_b64encode(hashed).rstrip(b"=").decode("utf-8")
    return code_verifier.decode("utf-8"), code_challenge

def get_authorization_url(code_challenge):
    """Constructs the Auth0 authorization URL."""
    authorize_url = f"https://{AUTH0_DOMAIN}/authorize?" \
                    f"response_type=code&" \
                    f"code_challenge={code_challenge}&" \
                    f"code_challenge_method=S256&" \
                    f"client_id={AUTH0_CLIENT_ID}&" \
                    f"redirect_uri={AUTH0_CALLBACK_URL}&" \
                    f"scope=openid%20profile%20email"
    return authorize_url

def exchange_code_for_token(code, code_verifier):
    """Exchanges the authorization code for an access token using PKCE."""
    token_url = f"https://{AUTH0_DOMAIN}/oauth/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "authorization_code",
        "client_id": AUTH0_CLIENT_ID,
        "code_verifier": code_verifier,
        "code": code,
        "redirect_uri": AUTH0_CALLBACK_URL,
    }
    response = requests.post(token_url, headers=headers, data=data)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    print("PKCE Login Flow Example (Auth0)")

    code_verifier, code_challenge = generate_pkce_challenge()
    print(f"Code Verifier: {code_verifier}")
    print(f"Code Challenge: {code_challenge}")

    authorization_url = get_authorization_url(code_challenge)
    print(f"Please open the following URL in your browser to authorize: {authorization_url}")

    # In a real application, you would now wait for the user to be redirected
    # back to AUTH0_CALLBACK_URL with a 'code' query parameter.
    # For this example, we'll simulate receiving a code.
    print("
--- SIMULATING AUTHORIZATION REDIRECTION ---")
    simulated_code = input("Enter the authorization code from the redirect URL (e.g., 'YOUR_AUTH_CODE'): ")

    if simulated_code:
        try:
            token_response = exchange_code_for_token(simulated_code, code_verifier)
            print("
Successfully exchanged code for tokens:")
            print(json.dumps(token_response, indent=2))
            access_token = token_response.get("access_token")
            if access_token:
                print(f"
Access Token: {access_token}")
                # You can now use the access_token to call protected APIs
        except requests.exceptions.HTTPError as e:
            print(f"Error exchanging code for token: {e}")
            if e.response:
                print(f"Response: {e.response.json()}")
    else:
        print("No authorization code provided. Exiting.")
