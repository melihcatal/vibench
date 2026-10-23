import os
import urllib.parse
import hashlib
import base64
import requests
import json

AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID")
AUTH0_CALLBACK_URL = os.environ.get("AUTH0_CALLBACK_URL")


def generate_pkce_challenge():
    code_verifier = (
        base64.urlsafe_b64encode(os.urandom(32)).rstrip(b"=").decode("utf-8")
    )
    code_challenge = (
        base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode("utf-8")).digest())
        .rstrip(b"=")
        .decode("utf-8")
    )
    return code_verifier, code_challenge


def start_pkce_login_flow(code_challenge: str):
    authorize_url = f"https://{AUTH0_DOMAIN}/authorize"
    params = {
        "response_type": "code",
        "client_id": AUTH0_CLIENT_ID,
        "redirect_uri": AUTH0_CALLBACK_URL,
        "scope": "openid profile email",
        "audience": f"https://{AUTH0_DOMAIN}/api/v2/",
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    }
    return f"{authorize_url}?{urllib.parse.urlencode(params)}"


def exchange_pkce_code_for_tokens(authorization_code: str, code_verifier: str):
    token_url = f"https://{AUTH0_DOMAIN}/oauth/token"
    headers = {"content-type": "application/x-www-form-urlencoded"}
    payload = {
        "grant_type": "authorization_code",
        "client_id": AUTH0_CLIENT_ID,
        "code": authorization_code,
        "redirect_uri": AUTH0_CALLBACK_URL,
        "code_verifier": code_verifier,
    }
    response = requests.post(token_url, headers=headers, data=payload)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    # Example usage:
    # Set environment variables AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_CALLBACK_URL
    # code_verifier, code_challenge = generate_pkce_challenge()
    # login_url = start_pkce_login_flow(code_challenge)
    # print(f"Redirect user to: {login_url}")
    # Simulate callback
    # auth_code = "YOUR_AUTHORIZATION_CODE_FROM_REDIRECT"
    # tokens = exchange_pkce_code_for_tokens(auth_code, code_verifier)
    # print(json.dumps(tokens, indent=2))
    pass
