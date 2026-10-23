import os
import base64
import hashlib
import secrets
from urllib.parse import urlencode
from identity_client import (
    get_auth0_config,
    build_auth0_authorize_url,
    build_auth0_token_url,
)
import requests


def generate_pkce_pair():
    code_verifier = secrets.token_urlsafe(64)
    hashed = hashlib.sha256(code_verifier.encode("utf-8")).digest()
    code_challenge = base64.urlsafe_b64encode(hashed).decode("utf-8").replace("=", "")
    return code_verifier, code_challenge


def start_pkce_login():
    config = get_auth0_config()
    if not config["DOMAIN"] or not config["CLIENT_ID"] or not config["CALLBACK_URL"]:
        raise ValueError("Auth0 configuration environment variables are not set.")

    code_verifier, code_challenge = generate_pkce_pair()
    state = str(secrets.token_urlsafe(16))

    # In a real application, store these securely in a session linked to the state
    os.environ["OAUTH_STATE"] = state
    os.environ["PKCE_CODE_VERIFIER"] = code_verifier

    authorization_url = build_auth0_authorize_url(config, state, code_challenge)
    print(f"Redirect to: {authorization_url}")
    return authorization_url


def exchange_pkce_code_for_tokens(code: str, state: str) -> dict:
    expected_state = os.getenv("OAUTH_STATE")
    code_verifier = os.getenv("PKCE_CODE_VERIFIER")

    if not expected_state or state != expected_state:
        raise ValueError("State mismatch. Possible CSRF attack.")
    if not code_verifier:
        raise ValueError("Code verifier not found in session. PKCE flow compromised.")

    config = get_auth0_config()
    if not config["DOMAIN"] or not config["CLIENT_ID"] or not config["CALLBACK_URL"]:
        raise ValueError("Auth0 configuration environment variables are not set.")

    token_url = build_auth0_token_url(config)
    headers = {"content-type": "application/x-www-form-urlencoded"}
    payload = {
        "grant_type": "authorization_code",
        "client_id": config["CLIENT_ID"],
        "code_verifier": code_verifier,
        "code": code,
        "redirect_uri": config["CALLBACK_URL"],
    }

    response = requests.post(token_url, headers=headers, data=payload)
    response.raise_for_status()

    tokens = response.json()
    # Clean up stored verifier and state after successful exchange
    os.environ.pop("OAUTH_STATE", None)
    os.environ.pop("PKCE_CODE_VERIFIER", None)
    return tokens


if __name__ == "__main__":
    # Example usage: simulate starting a PKCE login
    # Set dummy environment variables for demonstration
    os.environ["AUTH0_DOMAIN"] = "YOUR_AUTH0_DOMAIN.auth0.com"
    os.environ["AUTH0_CLIENT_ID"] = "YOUR_AUTH0_CLIENT_ID"
    os.environ["AUTH0_CALLBACK_URL"] = "http://localhost:3000/pkce_callback"

    print("Starting PKCE login flow...")
    login_url = start_pkce_login()
    print(f"Please open this URL in your browser: {login_url}")
    print(f"Stored state: {os.getenv('OAUTH_STATE')}")
    print(f"Stored code verifier: {os.getenv('PKCE_CODE_VERIFIER')}")

    # Simulate callback after user grants authorization
    print("\nSimulating PKCE callback with a dummy code...")
    simulated_code = "dummy_pkce_auth_code"
    simulated_state = os.getenv("OAUTH_STATE")  # Use the stored state

    try:
        pkce_tokens = exchange_pkce_code_for_tokens(simulated_code, simulated_state)
        print("Successfully exchanged PKCE code for tokens:")
        print(pkce_tokens)
    except ValueError as e:
        print(f"Error during PKCE token exchange: {e}")
    except requests.exceptions.HTTPError as e:
        print(
            f"HTTP Error during PKCE token exchange: {e.response.status_code} - {e.response.text}"
        )
