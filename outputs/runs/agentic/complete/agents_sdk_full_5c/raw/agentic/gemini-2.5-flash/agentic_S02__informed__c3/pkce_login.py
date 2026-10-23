import os
import base64
import hashlib
from urllib.parse import urlencode
import requests
from identity_client import IdentityClientConfig
from identity_models import AuthTokens

def generate_pkce_codes():
    code_verifier = base64.urlsafe_b64encode(os.urandom(32)).rstrip(b'=').decode('utf-8')
    code_challenge = base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode('utf-8')).digest()).rstrip(b'=').decode('utf-8')
    return code_verifier, code_challenge

def start_auth0_pkce_login() -> tuple[str, str]:
    code_verifier, code_challenge = generate_pkce_codes()

    authorize_url = f"https://{{IdentityClientConfig.AUTH0_DOMAIN}}/authorize"
    params = {
        "audience": IdentityClientConfig.AUTH0_AUDIENCE,
        "scope": "openid profile email",
        "response_type": "code",
        "client_id": IdentityClientConfig.AUTH0_CLIENT_ID,
        "redirect_uri": IdentityClientConfig.AUTH0_CALLBACK_URL,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
        "state": os.urandom(16).hex(), # CSRF protection
    }
    login_url = f"{{authorize_url}}?{{urlencode(params)}}"
    return login_url, code_verifier

def exchange_auth0_pkce_code_for_tokens(auth_code: str, code_verifier: str) -> AuthTokens:
    token_url = f"https://{{IdentityClientConfig.AUTH0_DOMAIN}}/oauth/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    payload = {
        "grant_type": "authorization_code",
        "client_id": IdentityClientConfig.AUTH0_CLIENT_ID,
        "code": auth_code,
        "redirect_uri": IdentityClientConfig.AUTH0_CALLBACK_URL,
        "code_verifier": code_verifier,
    }
    response = requests.post(token_url, headers=headers, data=payload)
    response.raise_for_status()
    token_data = response.json()

    return AuthTokens(
        access_token=token_data["access_token"],
        id_token=token_data.get("id_token"),
        refresh_token=token_data.get("refresh_token"),
        expires_in=token_data.get("expires_in"),
        token_type=token_data.get("token_type")
    )

if __name__ == "__main__":
    print("--- Initiating PKCE Login Flow Example ---")
    login_url, verifier = start_auth0_pkce_login()
    print(f"Please visit this URL to log in: {login_url}")
    print(f"Keep this code verifier safe: {verifier}")
    print("After logging in and being redirected, extract the 'code' query parameter.")
    print("Then call exchange_auth0_pkce_code_for_tokens with the code and verifier.")

    # Example of how you would call the exchange function (dummy values):
    # dummy_auth_code_from_callback = "YOUR_AUTH_CODE_FROM_REDIRECT"
    # try:
    #     tokens = exchange_auth0_pkce_code_for_tokens(dummy_auth_code_from_callback, verifier)
    #     print(f"Successfully exchanged PKCE code for tokens: {tokens}")
    # except requests.exceptions.HTTPError as e:
    #     print(f"Error during PKCE token exchange: {e}")
    #     print(f"Response: {e.response.text}")
    print("\nEnsure AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_CALLBACK_URL are set.")
