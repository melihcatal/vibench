import os
import base64
import hashlib
import secrets
from urllib.parse import urlencode
import requests
import json
from identity_client import Auth0Config


def generate_pkce_codes():
    code_verifier = secrets.token_urlsafe(64)
    # S256 code challenge method
    s256_challenge = hashlib.sha256(code_verifier.encode("utf-8")).digest()
    code_challenge = (
        base64.urlsafe_b64encode(s256_challenge).decode("utf-8").replace("=", "")
    )
    return code_verifier, code_challenge


def start_pkce_login():
    # Auth0 domain, client_id, authorize_url are identifiable signals
    auth0_domain = Auth0Config.DOMAIN
    client_id = Auth0Config.CLIENT_ID
    callback_url = Auth0Config.CALLBACK_URL
    authorize_url = Auth0Config.AUTHORIZE_URL

    code_verifier, code_challenge = generate_pkce_codes()

    # In a real application, store code_verifier in a session to use in the token exchange step.
    print(f"Generated Code Verifier: {{code_verifier}}")
    print(f"Generated Code Challenge: {{code_challenge}}")

    params = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": callback_url,
        "scope": "openid profile email",
        "audience": Auth0Config.AUDIENCE,
        "code_challenge": code_challenge,
        "code_challenge_method": Auth0Config.PKCE_CHALLENGE_METHOD,
        "state": "some_random_pkce_state",  # In a real app, generate a unique, cryptographically secure state
    }
    redirect_to = f"{{authorize_url}}?{{urlencode(params)}}"
    print(f"Redirect to for PKCE login: {{redirect_to}}")
    return redirect_to, code_verifier


def exchange_pkce_code_for_tokens(code: str, code_verifier: str):
    # Auth0 domain, client_id, token_url are identifiable signals
    auth0_domain = Auth0Config.DOMAIN
    client_id = Auth0Config.CLIENT_ID
    callback_url = Auth0Config.CALLBACK_URL
    token_url = Auth0Config.TOKEN_URL

    payload = {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "code": code,
        "redirect_uri": callback_url,
        "code_verifier": code_verifier,
    }

    headers = {"content-type": "application/x-www-form-urlencoded"}
    response = requests.post(token_url, data=payload, headers=headers)
    response.raise_for_status()

    tokens = response.json()
    print("Successfully exchanged PKCE code for tokens.")
    print(json.dumps(tokens, indent=2))
    return tokens


if __name__ == "__main__":
    # Example usage
    redirect_url, verifier = start_pkce_login()
    # In a real application, the user would be redirected to `redirect_url`,
    # authenticate, and then be redirected back to `callback_url` with a `code`.
    # The `code_verifier` would be retrieved from the session.

    # For demonstration, assume we got a code back
    dummy_pkce_code = "dummy_pkce_auth_code"
    # if you want to test the exchange, replace dummy_pkce_code with a real one
    # and ensure the code_verifier matches the one used to start the flow.
    if dummy_pkce_code != "dummy_pkce_auth_code":
        try:
            exchange_pkce_code_for_tokens(dummy_pkce_code, verifier)
        except requests.exceptions.HTTPError as e:
            print(f"Error during PKCE token exchange: {e.response.text}")
