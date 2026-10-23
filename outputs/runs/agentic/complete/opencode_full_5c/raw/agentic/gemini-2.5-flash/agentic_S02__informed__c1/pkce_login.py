import os
import base64
import hashlib
import secrets
import requests
from urllib.parse import urlencode, urljoin
from typing import Optional

from identity_client import IdentityClient
from identity_models import OAuthTokenResponse


def generate_pkce_codes():
    """Generates PKCE code_verifier and code_challenge."""
    code_verifier = secrets.token_urlsafe(
        96
    )  # Generate a high-entropy cryptographic random string
    # S256 code_challenge method
    s256_hash = hashlib.sha256(code_verifier.encode("utf-8")).digest()
    code_challenge = (
        base64.urlsafe_b64encode(s256_hash).decode("utf-8").replace("=", "")
    )
    return code_verifier, code_challenge


def start_pkce_login(
    scope: str = "openid profile email", state: str = "pkce_state_string"
):
    """Starts a PKCE login flow for public clients using Auth0."""
    client = IdentityClient()
    code_verifier, code_challenge = generate_pkce_codes()

    authorize_url = client.get_authorize_url(
        scope=scope,
        state=state,
        code_challenge=code_challenge,
        code_challenge_method="S256",
    )
    print(f"Please redirect your user to: {authorize_url}")
    return (
        authorize_url,
        code_verifier,
    )  # Return code_verifier to be used in token exchange


def exchange_pkce_code_for_tokens(
    code: str, code_verifier: str
) -> Optional[OAuthTokenResponse]:
    """Exchanges the authorization code for tokens using PKCE with Auth0."""
    client = IdentityClient()
    token_url = client.get_token_url()

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "authorization_code",
        "client_id": client.auth0_client_id,
        "code_verifier": code_verifier,
        "code": code,
        "redirect_uri": client.redirect_uri,
    }

    try:
        response = requests.post(token_url, headers=headers, data=data)
        response.raise_for_status()
        token_data = response.json()
        return OAuthTokenResponse(
            access_token=token_data.get("access_token"),
            id_token=token_data.get("id_token"),
            refresh_token=token_data.get("refresh_token"),
            token_type=token_data.get("token_type", "Bearer"),
            expires_in=token_data.get("expires_in", 3600),
        )
    except requests.exceptions.RequestException as e:
        print(f"Error exchanging PKCE code for tokens: {e}")
        print(f"Response content: {response.text if response else 'No response'}")
        return None


if __name__ == "__main__":
    # Example usage (in a real application, this would be part of a web request handler)
    # Set environment variables for AUTH0_DOMAIN and AUTH0_CLIENT_ID before running
    # os.environ["AUTH0_DOMAIN"] = "YOUR_AUTH0_DOMAIN"
    # os.environ["AUTH0_CLIENT_ID"] = "YOUR_AUTH0_CLIENT_ID"
    # os.environ["AUTH0_REDIRECT_URI"] = "http://localhost:8080/pkce_callback"
    #
    # try:
    #     auth_url, verifier = start_pkce_login()
    #     print(f"Auth0 PKCE Authorization URL: {auth_url}")
    #     print(f"Please save this code_verifier for the token exchange: {verifier}")
    #     # In a real app, you would redirect the user and then on the callback endpoint,
    #     # you'd use the 'code' from the URL and the saved 'verifier' to get tokens.
    #     # For demonstration, simulate the callback with a dummy code:
    #     # dummy_code_from_redirect = "some_pkce_auth_code"
    #     # tokens = exchange_pkce_code_for_tokens(dummy_code_from_redirect, verifier)
    #     # if tokens:
    #     #     print(f"PKCE Tokens: {tokens.access_token[:10]}...")
    #     # else:
    #     #     print("PKCE token exchange failed.")
    # except ValueError as e:
    #     print(f"Error: {e}")
    pass  # placeholder to avoid runtime error if __name__ is run without actual env vars
