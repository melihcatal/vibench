import os
import requests
from urllib.parse import urlencode

from identity_client import IdentityClient
from identity_models import TokenResponse

def oauth_callback(code: str, state: str, redirect_uri: str) -> TokenResponse:
    """Handles the OAuth callback and exchanges an authorization code for tokens.

    Args:
        code: The authorization code received from the identity provider.
        state: The state parameter received from the identity provider.
               This should be validated against the stored state.
        redirect_uri: The URI used to initiate the login flow.

    Returns:
        A TokenResponse object containing access, refresh, and ID tokens.
    """
    client = IdentityClient()

    # In a real application, validate the 'state' parameter against the stored state
    # to prevent CSRF attacks. For simplicity, we're skipping full validation here.
    # assert state == stored_oauth_state.session_id

    token_params = {
        "client_id": client.client_id,
        "scope": client.scope,
        "code": code,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
        "client_secret": client.client_secret, # Required for confidential clients
    }

    response = requests.post(client.token_endpoint, data=token_params)
    response.raise_for_status()
    token_data = response.json()

    return TokenResponse(
        access_token=token_data["access_token"],
        refresh_token=token_data.get("refresh_token"),
        id_token=token_data.get("id_token"),
        token_type=token_data["token_type"],
        expires_in=token_data["expires_in"],
    )

if __name__ == '__main__':
    # Example usage (replace with actual code, state, and redirect_uri)
    # This part would typically be called by your web application after the redirect.
    # For demonstration purposes, assume you received a code and state.
    example_code = "<YOUR_AUTHORIZATION_CODE>"
    example_state = "<YOUR_STATE_FROM_INITIAL_LOGIN>"
    example_redirect_uri = "http://localhost:8000/oauth_callback"

    if example_code == "<YOUR_AUTHORIZATION_CODE>":
        print("Please replace <YOUR_AUTHORIZATION_CODE> with a real code from Azure AD.")
    elif example_state == "<YOUR_STATE_FROM_INITIAL_LOGIN>":
        print("Please replace <YOUR_STATE_FROM_INITIAL_LOGIN> with the state from initial login.")
    else:
        try:
            token_response = oauth_callback(example_code, example_state, example_redirect_uri)
            print("Successfully exchanged code for tokens:")
            print(f"Access Token: {token_response.access_token[:30]}...")
            print(f"ID Token: {token_response.id_token[:30]}...")
        except requests.exceptions.HTTPError as e:
            print(f"Error during token exchange: {e.response.status_code} - {e.response.text}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
