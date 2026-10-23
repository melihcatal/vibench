import os
import base64
import hashlib
import secrets
import urllib.parse
import requests
from identity_client import Auth0Config
from identity_models import UserProfile


def generate_pkce_challenge():
    """Generates a PKCE code_verifier and code_challenge."""
    code_verifier = secrets.token_urlsafe(64)
    s256 = hashlib.sha256()
    s256.update(code_verifier.encode("utf-8"))
    code_challenge = (
        base64.urlsafe_b64encode(s256.digest()).decode("utf-8").replace("=", "")
    )
    return code_verifier, code_challenge


def start_auth0_pkce_login():
    """
    Constructs the Auth0 authorization URL for a PKCE-enabled login flow.
    Returns the authorization URL and the code_verifier.
    """
    if not all([Auth0Config.DOMAIN, Auth0Config.CLIENT_ID, Auth0Config.CALLBACK_URL]):
        raise ValueError("Auth0 configuration environment variables are not set.")

    code_verifier, code_challenge = generate_pkce_challenge()

    params = {
        "response_type": "code",
        "client_id": Auth0Config.CLIENT_ID,
        "redirect_uri": Auth0Config.CALLBACK_URL,
        "scope": Auth0Config.SCOPE,
        "audience": Auth0Config.AUDIENCE,
        "state": "some_random_pkce_state",  # In a real app, generate and verify this.
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    }
    query_string = urllib.parse.urlencode(params)
    authorization_url = f"https://{Auth0Config.DOMAIN}/authorize?{query_string}"
    return authorization_url, code_verifier


def handle_auth0_pkce_callback(
    code: str, state: str, code_verifier: str
) -> UserProfile:
    """
    Handles the Auth0 callback for PKCE, exchanging the authorization code for tokens
    using the code_verifier, and fetching user profile information.
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

    # In a real app, verify the 'state' parameter.
    # if state != "some_random_pkce_state":
    #     raise ValueError("Invalid state parameter.")

    token_url = f"https://{Auth0Config.DOMAIN}/oauth/token"
    payload = {
        "grant_type": "authorization_code",
        "client_id": Auth0Config.CLIENT_ID,
        "client_secret": Auth0Config.CLIENT_SECRET,
        "code": code,
        "redirect_uri": Auth0Config.CALLBACK_URL,
        "code_verifier": code_verifier,
    }
    headers = {"Content-Type": "application/json"}

    response = requests.post(token_url, json=payload, headers=headers)
    response.raise_for_status()
    token_data = response.json()

    access_token = token_data.get("access_token")

    if not access_token:
        raise ValueError("Access token not received.")

    # Fetch user profile (can reuse logic from profile_claims.py or inline here)
    userinfo_url = f"https://{Auth0Config.DOMAIN}/userinfo"
    userinfo_headers = {"Authorization": f"Bearer {access_token}"}
    userinfo_response = requests.get(userinfo_url, headers=userinfo_headers)
    userinfo_response.raise_for_status()
    user_claims = userinfo_response.json()

    user_profile = UserProfile(
        sub=user_claims.get("sub"),
        email=user_claims.get("email"),
        name=user_claims.get("name"),
        picture=user_claims.get("picture"),
        normalized_claims=user_claims,
    )
    return user_profile


if __name__ == "__main__":
    print("This file implements a PKCE login flow for public clients.")
    print("To start:")
    print("  auth_url, verifier = start_auth0_pkce_login()")
    print("  print(f'Visit: {auth_url}')")
    print("  # After redirect with code:")
    print(
        "  # user_profile = handle_auth0_pkce_callback(code='YOUR_AUTH_CODE', state='some_random_pkce_state', code_verifier=verifier)"
    )
