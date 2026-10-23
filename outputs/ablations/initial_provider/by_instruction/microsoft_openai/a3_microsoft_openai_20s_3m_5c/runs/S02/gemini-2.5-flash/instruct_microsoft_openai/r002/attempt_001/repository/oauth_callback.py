import os
import requests
import urllib.parse
import json
from typing import Optional

import identity_client
from identity_models import TokenResponse

def handle_oauth_callback(authorization_code: str, pkce_code_verifier: Optional[str] = None) -> Optional[TokenResponse]:
    """Handles the OAuth callback and exchanges the authorization code for tokens."""
    token_data = {
        "client_id": identity_client.AZURE_AD_CLIENT_ID,
        "scope": " ".join(identity_client.AZURE_AD_SCOPES),
        "code": authorization_code,
        "redirect_uri": identity_client.AZURE_AD_REDIRECT_URI,
        "grant_type": "authorization_code",
    }

    if pkce_code_verifier:
        token_data["code_verifier"] = pkce_code_verifier

    try:
        response = requests.post(
            identity_client.AZURE_AD_TOKEN_ENDPOINT,
            data=token_data,
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )
        response.raise_for_status() # Raise an exception for HTTP errors

        token_response_json = response.json()
        token_response = TokenResponse(
            access_token=token_response_json["access_token"],
            token_type=token_response_json["token_type"],
            expires_in=token_response_json["expires_in"],
            scope=token_response_json["scope"],
            refresh_token=token_response_json.get("refresh_token"),
            id_token=token_response_json.get("id_token"),
            raw_response=token_response_json
        )
        print("Successfully exchanged authorization code for tokens.")
        # In a real application, you would store these tokens securely.
        return token_response

    except requests.exceptions.RequestException as e:
        print(f"Error during token exchange: {e}")
        if response is not None:
            print(f"Response content: {response.text}")
        return None

if __name__ == "__main__":
    # This part would typically be handled by a web framework
    # For demonstration, we simulate receiving a code
    print("To test this, run start_oauth_login.py, get the code from the redirect URL, and then run this script with the code.")
    example_authorization_code = os.environ.get("OAUTH_AUTH_CODE", "YOUR_AUTHORIZATION_CODE_HERE")
    if example_authorization_code == "YOUR_AUTHORIZATION_CODE_HERE":
        print("Please set the OAUTH_AUTH_CODE environment variable or replace the placeholder.")
    else:
        print(f"Attempting to exchange code: {example_authorization_code[:10]}...")
        tokens = handle_oauth_callback(example_authorization_code)
        if tokens:
            print(f"Access Token (first 20 chars): {tokens.access_token[:20]}...")
            if tokens.id_token:
                print(f"ID Token (first 20 chars): {tokens.id_token[:20]}...")
