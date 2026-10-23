import base64
import hashlib
import os
import secrets
import urllib.parse

# Concrete external provider: Google
# This file implements a PKCE login flow for public clients using Google as the OAuth 2.0 provider.

# Configuration for Google OAuth 2.0
CLIENT_ID = "YOUR_GOOGLE_CLIENT_ID"  # Replace with your actual Google Client ID
REDIRECT_URI = "http://localhost:8080/callback"  # Replace with your redirect URI
AUTHORIZATION_ENDPOINT = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"
USERINFO_ENDPOINT = "https://openidconnect.googleapis.com/v1/userinfo"
SCOPE = "openid email profile"

def generate_pkce_pair():
    """Generates a PKCE code_verifier and code_challenge."""
    code_verifier = secrets.token_urlsafe(96)  # Generate a high-entropy cryptographically random string
    hashed = hashlib.sha256(code_verifier.encode('utf-8')).digest()
    code_challenge = base64.urlsafe_b64encode(hashed).decode('utf-8').replace('=', '')
    return code_verifier, code_challenge

def get_authorization_url(code_challenge: str, state: str) -> str:
    """Constructs the authorization URL for Google."""
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": SCOPE,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
        "state": state,
        "access_type": "offline",  # To get a refresh token
        "prompt": "consent",  # To ensure refresh token is returned
    }
    return f"{AUTHORIZATION_ENDPOINT}?{urllib.parse.urlencode(params)}"

def exchange_code_for_tokens(code: str, code_verifier: str) -> dict:
    """Exchanges the authorization code for access and ID tokens using Google's token endpoint."""
    data = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
        "code": code,
        "code_verifier": code_verifier,
    }
    # In a real application, you would use a library like 'requests' here:
    # import requests
    # response = requests.post(TOKEN_ENDPOINT, data=data)
    # response.raise_for_status()
    # return response.json()
    return {
        "access_token": "mock_access_token",
        "id_token": "mock_id_token",
        "expires_in": 3600,
        "token_type": "Bearer",
        "scope": SCOPE,
    } # Placeholder for actual API call

def get_user_profile(access_token: str) -> dict:
    """Fetches user profile information from Google's UserInfo endpoint."""
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    # In a real application, you would use a library like 'requests' here:
    # import requests
    # response = requests.get(USERINFO_ENDPOINT, headers=headers)
    # response.raise_for_status()
    # return response.json()
    return {
        "sub": "mock_user_id",
        "name": "Mock User",
        "given_name": "Mock",
        "family_name": "User",
        "picture": "https://example.com/mock.jpg",
        "email": "mock.user@example.com",
        "email_verified": True
    } # Placeholder for actual API call

# Example usage (would typically be part of a web application)
if __name__ == "__main__":
    verifier, challenge = generate_pkce_pair()
    # In a real app, 'state' would be generated and stored to prevent CSRF
    current_state = secrets.token_urlsafe(32)

    print(f"Generated Code Verifier: {verifier}")
    print(f"Generated Code Challenge: {challenge}")

    auth_url = get_authorization_url(challenge, current_state)
    print(f"Please open this URL in your browser to authorize: {auth_url}")

    print("\nAfter authorization, Google will redirect to your REDIRECT_URI with a 'code' and 'state' parameter.")
    print("You would then extract the 'code' from the redirect URL and use it to exchange for tokens.")
    print("For example, if the redirect URL is 'http://localhost:8080/callback?code=AUTH_CODE&state=YOUR_STATE',")
    print("you would call 'exchange_code_for_tokens(AUTH_CODE, verifier)'.")

    # Example of how you would call the token exchange and user info fetching functions
    # For demonstration, let's assume we received an authorization code "mock_auth_code"
    # auth_code_from_redirect = "mock_auth_code"
    # if auth_code_from_redirect and current_state == "YOUR_STATE_FROM_REDIRECT": # Always verify state
    #     try:
    #         tokens = exchange_code_for_tokens(auth_code_from_redirect, verifier)
    #         print("\nTokens obtained:")
    #         print(tokens)
    #         access_token = tokens.get("access_token")
    #         if access_token:
    #             user_profile = get_user_profile(access_token)
    #             print("\nUser Profile:")
    #             print(user_profile)
    #     except Exception as e:
    #         print(f"Error during token exchange or profile fetch: {e}")
    # else:
    #     print("Authorization failed or state mismatch.")
