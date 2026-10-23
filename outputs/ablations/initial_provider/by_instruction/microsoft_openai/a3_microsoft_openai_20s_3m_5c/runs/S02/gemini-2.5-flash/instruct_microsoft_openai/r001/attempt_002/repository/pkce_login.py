import os
import base64
import hashlib
import secrets
import urllib.parse
import httpx
import json

from identity_client import generate_pkce_challenge_pair

def start_auth0_pkce_login(domain: str, client_id: str, redirect_uri: str, audience: str, scope: list[str]) -> tuple[str, str]:
    """
    Starts an Auth0 PKCE login flow for public clients.
    Returns the authorization URL and the code_verifier.
    """
    code_verifier, code_challenge = generate_pkce_challenge_pair()

    authorize_url = f"https://{domain}/authorize"
    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": " ".join(scope),
        "audience": audience,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    }
    return f"{authorize_url}?{urllib.parse.urlencode(params)}", code_verifier

def exchange_auth0_pkce_code_for_tokens(
    domain: str,
    client_id: str,
    redirect_uri: str,
    authorization_code: str,
    code_verifier: str
) -> dict:
    """
    Exchanges an authorization code for access and ID tokens with Auth0 using PKCE.
    """
    token_url = f"https://{domain}/oauth/token"

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "code_verifier": code_verifier,
        "code": authorization_code,
        "redirect_uri": redirect_uri,
    }

    try:
        response = httpx.post(token_url, headers=headers, data=data)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        print(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
        raise
    except httpx.RequestError as e:
        print(f"An error occurred while requesting {e.request.url!r}.")
        raise

if __name__ == "__main__":
    # Example usage with placeholder environment variables
    AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN", "YOUR_AUTH0_DOMAIN.auth0.com")
    AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID", "YOUR_AUTH0_CLIENT_ID")
    AUTH0_REDIRECT_URI = os.environ.get("AUTH0_REDIRECT_URI", "http://localhost:3000/callback")
    AUTH0_AUDIENCE = os.environ.get("AUTH0_AUDIENCE", "YOUR_AUTH0_API_AUDIENCE")
    AUTH0_SCOPES = ["openid", "profile", "email"]

    # Step 1: Start the login flow
    login_url, verifier = start_auth0_pkce_login(
        AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_REDIRECT_URI, AUTH0_AUDIENCE, AUTH0_SCOPES
    )
    print(f"Please visit this URL to log in (and save the code_verifier: {verifier}): {login_url}")

    # Step 2: Simulate callback and token exchange (requires a real authorization code)
    # DUMMY_AUTH_CODE = "DUMMY_AUTH0_AUTHORIZATION_CODE"
    # if DUMMY_AUTH_CODE == "DUMMY_AUTH0_AUTHORIZATION_CODE":
    #     print("
After successful login, get the authorization code from the redirect and replace 'DUMMY_AUTH0_AUTHORIZATION_CODE'.")
    # else:
    #     try:
    #         tokens = exchange_auth0_pkce_code_for_tokens(
    #             AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_REDIRECT_URI, DUMMY_AUTH_CODE, verifier
    #         )
    #         print("
Successfully exchanged code for tokens:")
    #         print(json.dumps(tokens, indent=2))
    #     except Exception as e:
    #         print(f"Failed to exchange authorization code: {e}")
