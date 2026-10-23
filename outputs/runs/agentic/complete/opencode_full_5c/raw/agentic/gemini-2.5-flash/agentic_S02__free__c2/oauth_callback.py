import os
import requests
import json
from identity_client import Auth0Config


def oauth_callback(code: str, state: str):
    # Auth0 domain, client_id, client_secret, and token_url are identifiable signals
    auth0_domain = Auth0Config.DOMAIN
    client_id = Auth0Config.CLIENT_ID
    client_secret = Auth0Config.CLIENT_SECRET
    callback_url = Auth0Config.CALLBACK_URL
    token_url = Auth0Config.TOKEN_URL

    # In a real app, validate the 'state' parameter against the one sent in start_oauth_login
    # if state != "expected_state":
    #     raise ValueError("Invalid state parameter")

    payload = {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
        "redirect_uri": callback_url,
    }

    headers = {"content-type": "application/x-www-form-urlencoded"}
    response = requests.post(token_url, data=payload, headers=headers)
    response.raise_for_status()

    tokens = response.json()
    print("Successfully exchanged code for tokens.")
    print(json.dumps(tokens, indent=2))
    return tokens


if __name__ == "__main__":
    # Example usage (replace with actual code and state from a real callback)
    # For demonstration, we'll use dummy values. In a real scenario, these come from the redirect URL.
    dummy_code = "dummy_auth_code_from_auth0"
    dummy_state = "some_random_state_string"
    try:
        oauth_callback(dummy_code, dummy_state)
    except requests.exceptions.HTTPError as e:
        print(f"Error during token exchange: {e.response.text}")
    except ValueError as e:
        print(f"Error: {e}")
