import os
import requests
import json
from identity_client import Auth0Config
from identity_models import UserProfile


def handle_auth0_callback(code: str, state: str) -> UserProfile:
    """
    Handles the Auth0 callback, exchanging the authorization code for tokens
    and fetching user profile information.
    """
    if not all(
        [
            Auth0Config.DOMAIN,
            Auth0Config.CLIENT_ID,
            Auth0Config.CLIENT_SECRET,
            Auth0Config.CALLBACK_URL,
        ]
    ):
        raise ValueError("Auth0 configuration environment variables are not set.")

    # In a real app, verify the 'state' parameter against the one sent in start_oauth_login.py
    # if state != "some_random_state":
    #     raise ValueError("Invalid state parameter.")

    token_url = f"https://{Auth0Config.DOMAIN}/oauth/token"
    payload = {
        "grant_type": "authorization_code",
        "client_id": Auth0Config.CLIENT_ID,
        "client_secret": Auth0Config.CLIENT_SECRET,
        "code": code,
        "redirect_uri": Auth0Config.CALLBACK_URL,
    }
    headers = {"Content-Type": "application/json"}

    response = requests.post(token_url, json=payload, headers=headers)
    response.raise_for_status()
    token_data = response.json()

    access_token = token_data.get("access_token")
    id_token = token_data.get("id_token")

    if not access_token:
        raise ValueError("Access token not received.")

    # Fetch user profile
    userinfo_url = f"https://{Auth0Config.DOMAIN}/userinfo"
    userinfo_headers = {"Authorization": f"Bearer {access_token}"}
    userinfo_response = requests.get(userinfo_url, headers=userinfo_headers)
    userinfo_response.raise_for_status()
    user_claims = userinfo_response.json()

    # Normalize claims to a UserProfile object (simplified)
    user_profile = UserProfile(
        sub=user_claims.get("sub"),
        email=user_claims.get("email"),
        name=user_claims.get("name"),
        picture=user_claims.get("picture"),
        normalized_claims=user_claims,
    )
    return user_profile


if __name__ == "__main__":
    # Example usage (replace with actual code and state from a redirect)
    # This part would typically be called by a web framework at the callback URI
    print(
        "This file handles the OAuth callback. It expects 'code' and 'state' as input."
    )
    print(
        "Example: user_profile = handle_auth0_callback(code='YOUR_AUTH_CODE', state='some_random_state')"
    )
