import os
import requests
from typing import Dict, Any
from identity_client import (
    GOOGLE_CLIENT_ID,
    GOOGLE_CLIENT_SECRET,
    GOOGLE_REDIRECT_URI,
    GOOGLE_TOKEN_URL,
)
from identity_models import OAuthTokens


def handle_oauth_callback(code: str, state: str) -> OAuthTokens:
    # In a real application, 'state' would be verified against the stored state
    # from the start_oauth_login phase to prevent CSRF attacks.
    # For this example, we'll assume state verification passes.
    print(f"Received code: {code}, state: {state}")

    token_exchange_payload = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }

    response = requests.post(GOOGLE_TOKEN_URL, data=token_exchange_payload)
    response.raise_for_status()  # Raise an exception for HTTP errors
    token_data: Dict[str, Any] = response.json()

    # Google-specific: id_token is often present with openid scope
    oauth_tokens = OAuthTokens(
        access_token=token_data["access_token"],
        token_type=token_data["token_type"],
        expires_in=token_data["expires_in"],
        id_token=token_data.get("id_token"),
        refresh_token=token_data.get("refresh_token"),
        scope=token_data.get("scope"),
    )
    return oauth_tokens


if __name__ == "__main__":
    # This is a placeholder for demonstration. In a real scenario, these values
    # would come from the incoming request to the callback URL.
    example_code = "YOUR_AUTHORIZATION_CODE"
    example_state = "YOUR_STATE_FROM_START_OAUTH"

    try:
        tokens = handle_oauth_callback(example_code, example_state)
        print("Successfully exchanged code for tokens:")
        print(f"Access Token: {tokens.access_token[:10]}...")
        print(
            f"ID Token: {tokens.id_token[:10]}..." if tokens.id_token else "No ID Token"
        )
    except requests.exceptions.HTTPError as e:
        print(
            f"Error during token exchange: {e.response.status_code} - {e.response.text}"
        )
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
