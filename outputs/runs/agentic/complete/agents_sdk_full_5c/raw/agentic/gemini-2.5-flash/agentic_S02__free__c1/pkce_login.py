import os
import hashlib
import base64
import requests
import json

from identity_client import OKTA_ORG_URL, OKTA_CLIENT_ID, OKTA_REDIRECT_URI

def generate_pkce_challenge():
    """Generates PKCE code_verifier and code_challenge."""
    code_verifier = base64.urlsafe_b64encode(os.urandom(32)).rstrip(b'=').decode('utf-8')
    s256 = hashlib.sha256(code_verifier.encode('utf-8')).digest()
    code_challenge = base64.urlsafe_b64encode(s256).rstrip(b'=').decode('utf-8')
    return code_verifier, code_challenge

def start_pkce_login_flow():
    """
    Starts an Okta PKCE login flow for public clients.
    Returns the authorization URL and the code_verifier.
    """
    code_verifier, code_challenge = generate_pkce_challenge()

    scope = "openid profile email"
    state = os.urandom(16).hex() # CSRF protection
    nonce = os.urandom(16).hex() # Replay protection

    authorization_url = (
        f"{OKTA_ORG_URL}/oauth2/default/v1/authorize?"
        f"response_type=code&"
        f"client_id={OKTA_CLIENT_ID}&"
        f"redirect_uri={OKTA_REDIRECT_URI}&"
        f"scope={scope}&"
        f"state={state}&"
        f"nonce={nonce}&"
        f"code_challenge={code_challenge}&"
        f"code_challenge_method=S256"
    )
    return authorization_url, code_verifier

def exchange_pkce_code_for_tokens(authorization_code: str, code_verifier: str, state: str):
    """
    Exchanges the authorization code for tokens using PKCE.
    """
    # Validate the 'state' parameter against the one sent in start_pkce_login_flow.
    # For simplicity, this example doesn't implement state validation.

    token_url = f"{OKTA_ORG_URL}/oauth2/default/v1/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "authorization_code",
        "code": authorization_code,
        "redirect_uri": OKTA_REDIRECT_URI,
        "client_id": OKTA_CLIENT_ID,
        "code_verifier": code_verifier,
    }

    try:
        response = requests.post(token_url, headers=headers, data=data)
        response.raise_for_status() # Raise an exception for HTTP errors
        token_data = response.json()

        id_token = token_data.get("id_token")
        access_token = token_data.get("access_token")
        refresh_token = token_data.get("refresh_token")

        print("Successfully exchanged code for tokens using PKCE.")
        print(f"ID Token: {id_token[:30]}...")
        print(f"Access Token: {access_token[:30]}...")

        return {
            "id_token": id_token,
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
    except requests.exceptions.RequestException as e:
        print(f"Error exchanging PKCE authorization code: {e}")
        if response is not None:
            print(f"Response content: {response.text}")
        raise

if __name__ == "__main__":
    # Step 1: Start the PKCE flow
    auth_url, verifier = start_pkce_login_flow()
    print(f"Please visit this URL to start the Okta PKCE login: {auth_url}")
    print(f"Save this code_verifier for the callback: {verifier}")

    # Step 2: Simulate callback (replace with actual code and state from URL)
    print("
--- Simulate Callback ---")
    retrieved_code = input("Enter the 'code' from the redirected URL: ")
    retrieved_state = input("Enter the 'state' from the redirected URL: ")
    retrieved_verifier = input(f"Enter the code_verifier you saved (should be: {verifier}): ")

    if not retrieved_code or not retrieved_state or not retrieved_verifier:
        print("Skipping token exchange as input was not provided.")
    elif retrieved_verifier != verifier:
        print("Error: Code verifier mismatch! PKCE flow aborted.")
    else:
        try:
            tokens = exchange_pkce_code_for_tokens(retrieved_code, retrieved_verifier, retrieved_state)
            print("Tokens received:", tokens)
        except Exception as e:
            print(f"Failed to complete PKCE login: {e}")
