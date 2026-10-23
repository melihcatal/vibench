import os
import requests
from typing import Optional

from identity_client import IdentityClientConfig
from identity_models import TokenExchangeRequest, TokenResponse

def handle_oauth_callback(
    authorization_code: str,
    state: str,
    session_state: str, # In a real app, this would come from the user's session
    code_verifier: Optional[str] = None # For PKCE
) -> Optional[TokenResponse]:

    # In a real application, verify the 'state' parameter against the one stored in the session
    if state != session_state:
        print("CSRF attack detected: State mismatch.")
        return None

    token_request = TokenExchangeRequest(
        client_id=IdentityClientConfig.AZURE_AD_CLIENT_ID,
        client_secret=IdentityClientConfig.AZURE_AD_CLIENT_SECRET,
        redirect_uri=IdentityClientConfig.REDIRECT_URI,
        code=authorization_code,
        grant_type="authorization_code",
        code_verifier=code_verifier
    )

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "client_id": token_request.client_id,
        "redirect_uri": token_request.redirect_uri,
        "code": token_request.code,
        "grant_type": token_request.grant_type,
    }
    if token_request.client_secret:
        data["client_secret"] = token_request.client_secret
    if token_request.code_verifier:
        data["code_verifier"] = token_request.code_verifier

    try:
        response = requests.post(IdentityClientConfig.AZURE_AD_TOKEN_ENDPOINT, headers=headers, data=data)
        response.raise_for_status()
        token_data = response.json()
        print("Successfully exchanged authorization code for tokens.")
        return TokenResponse(**token_data)
    except requests.exceptions.RequestException as e:
        print(f"Error exchanging code for tokens: {e}")
        if response:
            print(f"Response content: {response.text}")
        return None

if __name__ == "__main__":
    # Example usage: Simulate a callback with a dummy code and state
    # In a real scenario, these values would come from the URL query parameters
    # and the user's session.
    dummy_auth_code = "dummy_authorization_code_from_azure_ad"
    dummy_state = "example_state_from_session_for_verification"
    # Set dummy environment variables for demonstration
    # os.environ["AZURE_AD_CLIENT_ID"] = "YOUR_AZURE_AD_CLIENT_ID"
    # os.environ["AZURE_AD_CLIENT_SECRET"] = "YOUR_AZURE_AD_CLIENT_SECRET"
    # os.environ["REDIRECT_URI"] = "http://localhost:8000/oauth/callback"

    print(f"Simulating OAuth callback with code: {dummy_auth_code} and state: {dummy_state}")
    # For this simulation, the session_state is the same as the dummy_state
    token_response = handle_oauth_callback(dummy_auth_code, dummy_state, dummy_state)

    if token_response:
        print(f"Access Token: {token_response.access_token[:10]}...")
        print(f"ID Token: {token_response.id_token[:10]}..." if token_response.id_token else "No ID Token")
