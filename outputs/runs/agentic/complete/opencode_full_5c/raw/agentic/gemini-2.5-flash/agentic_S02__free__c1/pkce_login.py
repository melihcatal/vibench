import os
import base64
import hashlib
import secrets
import requests
from typing import Tuple, Dict, Any
from identity_client import (
    GOOGLE_CLIENT_ID,
    GOOGLE_REDIRECT_URI,
    GOOGLE_AUTHORIZATION_URL,
    GOOGLE_TOKEN_URL,
)
from identity_models import OAuthTokens


def generate_pkce_codes() -> Tuple[str, str]:
    code_verifier = secrets.token_urlsafe(
        96
    )  # Generate a high-entropy cryptographically random string

    # Calculate the S256 (SHA256) hash of the code verifier
    s256_hash = hashlib.sha256(code_verifier.encode("utf-8")).digest()

    # Base64url-encode the hash
    code_challenge = (
        base64.urlsafe_b64encode(s256_hash).decode("utf-8").replace("=", "")
    )

    return code_verifier, code_challenge


def start_pkce_login() -> Tuple[str, str]:
    code_verifier, code_challenge = generate_pkce_codes()
    state = secrets.token_urlsafe(32)  # Google-specific state for CSRF protection

    scopes_str = "openid email profile"
    auth_url = (
        f"{GOOGLE_AUTHORIZATION_URL}?"
        + f"client_id={GOOGLE_CLIENT_ID}&"
        + f"redirect_uri={GOOGLE_REDIRECT_URI}&"
        + f"response_type=code&"
        + f"scope={scopes_str}&"
        + f"state={state}&"
        + f"code_challenge={code_challenge}&"
        + f"code_challenge_method=S256"
    )
    return (
        auth_url,
        code_verifier,
    )  # Return code_verifier to be stored in session for later token exchange


def exchange_pkce_code_for_tokens(code: str, code_verifier: str) -> OAuthTokens:
    token_exchange_payload = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
        "code_verifier": code_verifier,
    }
    # No client_secret for public clients in PKCE

    response = requests.post(GOOGLE_TOKEN_URL, data=token_exchange_payload)
    response.raise_for_status()  # Raise an exception for HTTP errors
    token_data: Dict[str, Any] = response.json()

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
    login_url, stored_code_verifier = start_pkce_login()
    print(f"Please visit this URL for PKCE login: {login_url}")
    print(f"Store this code verifier for the callback: {stored_code_verifier}")

    # In a real app, the code and state would come from the redirect callback
    # and the stored_code_verifier would be retrieved from the session.
    # For demonstration, assume we got a 'code' back.
    example_auth_code = "YOUR_AUTH_CODE_FROM_CALLBACK"
    if (
        example_auth_code != "YOUR_AUTH_CODE_FROM_CALLBACK"
    ):  # Only try if a real code is provided
        try:
            pkce_tokens = exchange_pkce_code_for_tokens(
                example_auth_code, stored_code_verifier
            )
            print("Successfully exchanged PKCE code for tokens:")
            print(f"Access Token: {pkce_tokens.access_token[:10]}...")
        except requests.exceptions.HTTPError as e:
            print(
                f"Error during PKCE token exchange: {e.response.status_code} - {e.response.text}"
            )
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
