import os
import requests
import json

from identity_client import AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET, AUTH0_CALLBACK_URL
from identity_models import TokenResponse

def exchange_code_for_tokens(code: str, state: str) -> TokenResponse:
    """
    Exchanges the authorization code received from Auth0 for access, ID, and refresh tokens.
    """
    token_url = f"https://{AUTH0_DOMAIN}/oauth/token"
    headers = {"content-type": "application/x-www-form-urlencoded"}
    payload = {
        "grant_type": "authorization_code",
        "client_id": AUTH0_CLIENT_ID,
        "client_secret": AUTH0_CLIENT_SECRET,
        "code": code,
        "redirect_uri": AUTH0_CALLBACK_URL,
    }

    try:
        response = requests.post(token_url, headers=headers, data=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        token_data = response.json()
        return TokenResponse(
            access_token=token_data.get("access_token"),
            id_token=token_data.get("id_token"),
            refresh_token=token_data.get("refresh_token"),
            token_type=token_data.get("token_type"),
            expires_in=token_data.get("expires_in")
        )
    except requests.exceptions.RequestException as e:
        print(f"Error exchanging code for tokens: {e}")
        raise

if __name__ == "__main__":
    # This is a simplified example. In a real application, 'code' and 'state'
    # would come from the incoming request query parameters.
    print("This script demonstrates token exchange. Run it with actual code and state from an OAuth callback.")
    # Example usage (replace with actual code and state)
    # try:
    #     dummy_code = "YOUR_AUTH_CODE_HERE"
    #     dummy_state = "YOUR_STATE_HERE"
    #     tokens = exchange_code_for_tokens(dummy_code, dummy_state)
    #     print("Successfully exchanged code for tokens:")
    #     print(json.dumps(tokens.to_dict(), indent=2))
    # except Exception as e:
    #     print(f"Failed to get tokens: {e}")
