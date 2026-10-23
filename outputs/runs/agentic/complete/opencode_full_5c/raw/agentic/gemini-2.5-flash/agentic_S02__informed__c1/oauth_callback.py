import os
import requests
import json
from typing import Optional
from identity_client import IdentityClient
from identity_models import OAuthTokenResponse


def handle_oauth_callback(
    code: str, state: str, expected_state: str
) -> Optional[OAuthTokenResponse]:
    """Handles the OAuth/OIDC callback and exchanges the authorization code for tokens using Auth0."""
    if state != expected_state:
        print("Error: State mismatch.")
        return None

    client = IdentityClient()
    token_url = client.get_token_url()

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "authorization_code",
        "client_id": client.auth0_client_id,
        "client_secret": client.auth0_client_secret,
        "code": code,
        "redirect_uri": client.redirect_uri,
    }

    try:
        response = requests.post(token_url, headers=headers, data=data)
        response.raise_for_status()
        token_data = response.json()
        return OAuthTokenResponse(
            access_token=token_data.get("access_token"),
            id_token=token_data.get("id_token"),
            refresh_token=token_data.get("refresh_token"),
            token_type=token_data.get("token_type", "Bearer"),
            expires_in=token_data.get("expires_in", 3600),
        )
    except requests.exceptions.RequestException as e:
        print(f"Error exchanging code for tokens: {e}")
        print(f"Response content: {response.text if response else 'No response'}")
        return None


if __name__ == "__main__":
    # Example usage (in a real application, code and state would come from the redirect URL)
    # Set environment variables for AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET, AUTH0_REDIRECT_URI
    # For testing, simulate a code and state
    # os.environ["AUTH0_DOMAIN"] = "YOUR_AUTH0_DOMAIN"
    # os.environ["AUTH0_CLIENT_ID"] = "YOUR_AUTH0_CLIENT_ID"
    # os.environ["AUTH0_CLIENT_SECRET"] = "YOUR_AUTH0_CLIENT_SECRET"
    # os.environ["AUTH0_REDIRECT_URI"] = "http://localhost:8080/callback"
    #
    # A dummy code and state for demonstration; in reality these come from the IdP redirect
    # dummy_code = "some_auth_code_from_idp"
    # dummy_state = "random_state_string"
    # expected_state_value = "random_state_string"
    #
    # tokens = handle_oauth_callback(dummy_code, dummy_state, expected_state_value)
    # if tokens:
    #     print(f"Successfully obtained tokens: {tokens.access_token[:10]}...")
    # else:
    #     print("Failed to obtain tokens.")
    pass  # placeholder to avoid runtime error if __name__ is run without actual env vars
