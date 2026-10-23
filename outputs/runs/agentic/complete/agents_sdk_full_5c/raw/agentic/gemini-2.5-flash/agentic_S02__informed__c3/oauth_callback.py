import requests
import os
from identity_client import IdentityClientConfig
from identity_models import AuthTokens

def handle_auth0_callback(auth_code: str, state: str) -> AuthTokens:
    token_url = f"https://{{IdentityClientConfig.AUTH0_DOMAIN}}/oauth/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    payload = {
        "grant_type": "authorization_code",
        "client_id": IdentityClientConfig.AUTH0_CLIENT_ID,
        "client_secret": IdentityClientConfig.AUTH0_CLIENT_SECRET,
        "code": auth_code,
        "redirect_uri": IdentityClientConfig.AUTH0_CALLBACK_URL,
    }
    response = requests.post(token_url, headers=headers, data=payload)
    response.raise_for_status()
    token_data = response.json()

    # In a real application, you would verify the 'state' parameter
    # with the one sent in start_oauth_login.py to prevent CSRF.
    # For this example, we'll assume it's verified.

    return AuthTokens(
        access_token=token_data["access_token"],
        id_token=token_data.get("id_token"),
        refresh_token=token_data.get("refresh_token"),
        expires_in=token_data.get("expires_in"),
        token_type=token_data.get("token_type")
    )

if __name__ == "__main__":
    # This is an example usage. In a real scenario, auth_code and state
    # would come from the URL query parameters of the callback request.
    # For demonstration, we'll use dummy values.
    dummy_auth_code = "YOUR_AUTHORIZATION_CODE_HERE"
    dummy_state = "YOUR_STATE_HERE"
    try:
        # Note: This will fail without a valid authorization code and a running Auth0 setup.
        # This block is purely for showing how the function would be called.
        # tokens = handle_auth0_callback(dummy_auth_code, dummy_state)
        # print(f"Successfully exchanged code for tokens: {tokens}")
        print("To test this, you need a valid authorization code and state from an Auth0 login flow.")
        print("Ensure AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET, AUTH0_CALLBACK_URL are set.")
    except requests.exceptions.HTTPError as e:
        print(f"Error during token exchange: {e}")
        print(f"Response: {e.response.text}")
