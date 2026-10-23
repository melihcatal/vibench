import os
import base64
import hashlib
import identity_client
import requests
import json

def generate_pkce_challenge():
    code_verifier = base64.urlsafe_b64encode(os.urandom(32)).rstrip(b"=").decode("utf-8")
    code_challenge = base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode("utf-8")).digest()).rstrip(b"=").decode("utf-8")
    return code_verifier, code_challenge

def start_pkce_login_flow():
    code_verifier, code_challenge = generate_pkce_challenge()
    auth_url = identity_client.get_google_auth_url(code_challenge=code_challenge)
    print(f"PKCE Code Verifier: {code_verifier}")
    print(f"PKCE Code Challenge: {code_challenge}")
    print(f"Redirecting to: {auth_url}")
    return auth_url, code_verifier

def exchange_pkce_code_for_tokens(code: str, code_verifier: str) -> dict:
    token_url = identity_client.GOOGLE_TOKEN_ENDPOINT
    redirect_uri = identity_client.GOOGLE_REDIRECT_URI
    client_id = identity_client.GOOGLE_CLIENT_ID

    data = {
        "code": code,
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "code_verifier": code_verifier,
        "grant_type": "authorization_code",
    }

    response = requests.post(token_url, data=data)
    response.raise_for_status()

    tokens = response.json()
    print("Successfully exchanged PKCE code for tokens.")
    return tokens

if __name__ == "__main__":
    # Step 1: Start the PKCE login flow
    auth_url_pkce, verifier = start_pkce_login_flow()

    # In a real application, the user would be redirected to auth_url_pkce, 
    # complete the login, and then be redirected back to the redirect_uri 
    # with an authorization 'code' in the query parameters.
    
    # Step 2: Simulate the callback and token exchange (using a placeholder code)
    print("\n--- Simulating token exchange with a placeholder code ---")
    example_auth_code = "YOUR_PKCE_AUTHORIZATION_CODE_HERE"
    try:
        pkce_tokens = exchange_pkce_code_for_tokens(example_auth_code, verifier)
        print(json.dumps(pkce_tokens, indent=2))
    except requests.exceptions.RequestException as e:
        print(f"Error during PKCE token exchange: {e}")
        if e.response:
            print(f"Response content: {e.response.text}")
