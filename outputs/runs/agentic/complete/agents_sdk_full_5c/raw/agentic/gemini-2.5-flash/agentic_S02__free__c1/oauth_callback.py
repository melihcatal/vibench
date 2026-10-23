import os
from okta.client import OktaClient
import requests

from identity_client import OKTA_ORG_URL, OKTA_CLIENT_ID, OKTA_CLIENT_SECRET, OKTA_REDIRECT_URI

def handle_oauth_callback(authorization_code: str, state: str):
    """
    Handles the OAuth/OIDC callback, exchanges the authorization code for tokens,
    and returns the ID and access tokens.
    """
    # Validate the 'state' parameter against the one sent in start_oauth_login.
    # For simplicity, this example doesn't implement state validation,
    # but it's crucial for security in a real application.

    token_url = f"{OKTA_ORG_URL}/oauth2/default/v1/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "authorization_code",
        "code": authorization_code,
        "redirect_uri": OKTA_REDIRECT_URI,
        "client_id": OKTA_CLIENT_ID,
        "client_secret": OKTA_CLIENT_SECRET,
    }

    try:
        response = requests.post(token_url, headers=headers, data=data)
        response.raise_for_status() # Raise an exception for HTTP errors
        token_data = response.json()

        id_token = token_data.get("id_token")
        access_token = token_data.get("access_token")
        refresh_token = token_data.get("refresh_token") # If requested and allowed

        print("Successfully exchanged code for tokens.")
        print(f"ID Token: {id_token[:30]}...")
        print(f"Access Token: {access_token[:30]}...")

        return {
            "id_token": id_token,
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
    except requests.exceptions.RequestException as e:
        print(f"Error exchanging authorization code: {e}")
        if response is not None:
            print(f"Response content: {response.text}")
        raise

if __name__ == "__main__":
    # Example usage (replace with a real authorization code and state)
    # In a web application, these would come from the request query parameters.
    example_code = "YOUR_AUTHORIZATION_CODE_HERE"
    example_state = "YOUR_STATE_HERE" # Must match the state sent in start_oauth_login

    if "YOUR_AUTHORIZATION_CODE_HERE" in example_code:
        print("Please replace 'YOUR_AUTHORIZATION_CODE_HERE' and 'YOUR_STATE_HERE' with actual values from an Okta callback.")
    else:
        try:
            tokens = handle_oauth_callback(example_code, example_state)
            print("Tokens received:", tokens)
        except Exception as e:
            print(f"Failed to handle callback: {e}")
