import os
import requests
import json
from typing import Dict, Any, Optional
from identity_client import Auth0Client
from identity_models import TokenResponse


def handle_oauth_callback(
    code: str, state: str, original_state: str, code_verifier: Optional[str] = None
) -> TokenResponse:
    """Handles the OAuth/OIDC callback and exchanges an authorization code for tokens."""
    if state != original_state:
        raise ValueError("CSRF attack detected: State mismatch.")

    client = Auth0Client()
    if not client.client_secret:
        raise ValueError(
            "AUTH0_CLIENT_SECRET must be set for authorization code exchange."
        )

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "authorization_code",
        "client_id": client.client_id,
        "client_secret": client.client_secret,
        "code": code,
        "redirect_uri": client.callback_url,
    }
    if code_verifier:
        data["code_verifier"] = code_verifier

    response = requests.post(client.get_token_url(), headers=headers, data=data)
    response.raise_for_status()  # Raise an exception for HTTP errors
    token_data = response.json()

    return TokenResponse(
        access_token=token_data["access_token"],
        id_token=token_data.get("id_token"),
        refresh_token=token_data.get("refresh_token"),
        expires_in=token_data.get("expires_in"),
        token_type=token_data.get("token_type", "Bearer"),
    )


# Example usage (not part of the file, just for demonstration):
# if __name__ == "__main__":
#     os.environ["AUTH0_DOMAIN"] = "YOUR_AUTH0_DOMAIN.auth0.com"
#     os.environ["AUTH0_CLIENT_ID"] = "YOUR_AUTH0_CLIENT_ID"
#     os.environ["AUTH0_CLIENT_SECRET"] = "YOUR_AUTH0_CLIENT_SECRET"
#     os.environ["AUTH0_CALLBACK_URL"] = "http://localhost:8000/callback"
#     # This would typically come from the redirect after user login
#     sample_code = "sample_auth_code_from_auth0"
#     sample_state = "the_same_state_sent_earlier"
#     original_state_stored_in_session = "the_same_state_sent_earlier"
#     try:
#         tokens = handle_oauth_callback(sample_code, sample_state, original_state_stored_in_session)
#         print(f"Access Token: {tokens.access_token}")
#     except requests.exceptions.HTTPError as e:
#         print(f"Error exchanging code: {e.response.text}")
#     except ValueError as e:
#         print(f"Error: {e}")
