import os
import base64
import hashlib
import requests
import secrets
from urllib.parse import urlencode
from identity_client import IdentityClientConfig
from identity_models import AuthTokens


def generate_pkce_challenge():
    code_verifier = secrets.token_urlsafe(96)  # Generate a random string
    # Hash the code verifier using SHA256
    s256 = hashlib.sha256(code_verifier.encode("utf-8")).digest()
    # Base64url-encode the hash
    code_challenge = base64.urlsafe_b64encode(s256).decode("utf-8").replace("=", "")
    return code_verifier, code_challenge


def start_okta_pkce_login() -> tuple[str, str]:
    code_verifier, code_challenge = generate_pkce_challenge()
    state = secrets.token_urlsafe(32)  # In a real app, store state securely

    params = {
        "client_id": IdentityClientConfig.OKTA_CLIENT_ID,
        "redirect_uri": IdentityClientConfig.OKTA_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "state": state,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    }
    auth_url = f"{IdentityClientConfig.OKTA_ISSUER}/v1/authorize?{urlencode(params)}"
    return (
        auth_url,
        code_verifier,
    )  # Return code_verifier to be stored for token exchange


def handle_okta_pkce_callback(code: str, code_verifier: str) -> AuthTokens:
    token_endpoint = f"{IdentityClientConfig.OKTA_ISSUER}/v1/token"
    token_params = {
        "grant_type": "authorization_code",
        "client_id": IdentityClientConfig.OKTA_CLIENT_ID,
        "redirect_uri": IdentityClientConfig.OKTA_REDIRECT_URI,
        "code": code,
        "code_verifier": code_verifier,
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    try:
        response = requests.post(token_endpoint, data=token_params, headers=headers)
        response.raise_for_status()
        token_data = response.json()

        return AuthTokens(
            access_token=token_data["access_token"],
            token_type=token_data["token_type"],
            expires_in=token_data["expires_in"],
            id_token=token_data.get("id_token"),
            refresh_token=token_data.get("refresh_token"),
        )
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to exchange code for tokens with Okta: {e}")


if __name__ == "__main__":
    # Example of starting the login flow
    login_url, stored_code_verifier = start_okta_pkce_login()
    print(f"Visit this URL for Okta PKCE login: {login_url}")
    print(f"Store this code verifier for later: {stored_code_verifier}")

    # Example of handling the callback (simulate receiving code and using stored verifier)
    example_auth_code = os.environ.get("EXAMPLE_OKTA_AUTH_CODE", "YOUR_OKTA_AUTH_CODE")
    example_code_verifier = os.environ.get(
        "EXAMPLE_OKTA_CODE_VERIFIER", stored_code_verifier
    )

    if example_auth_code != "YOUR_OKTA_AUTH_CODE":
        try:
            okta_tokens = handle_okta_pkce_callback(
                example_auth_code, example_code_verifier
            )
            print(f"Successfully retrieved Okta tokens: {okta_tokens}")
        except Exception as e:
            print(f"Error handling Okta PKCE callback: {e}")
    else:
        print(
            "Please set EXAMPLE_OKTA_AUTH_CODE and optionally EXAMPLE_OKTA_CODE_VERIFIER environment variables to test Okta callback."
        )
