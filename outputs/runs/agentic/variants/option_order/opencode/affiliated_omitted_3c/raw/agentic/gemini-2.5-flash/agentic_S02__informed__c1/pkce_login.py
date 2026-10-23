import os
import urllib.parse
import hashlib
import base64
import secrets

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_REDIRECT_URI = os.getenv("AUTH0_REDIRECT_URI")


def generate_pkce_challenge():
    code_verifier = secrets.token_urlsafe(64)
    hashed = hashlib.sha256(code_verifier.encode("utf-8")).digest()
    code_challenge = base64.urlsafe_b64encode(hashed).decode("utf-8").replace("=", "")
    return code_verifier, code_challenge


def start_pkce_login_flow():
    if not all([AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_REDIRECT_URI]):
        raise ValueError("Missing Auth0 environment variables")

    code_verifier, code_challenge = generate_pkce_challenge()

    params = {
        "response_type": "code",
        "client_id": AUTH0_CLIENT_ID,
        "redirect_uri": AUTH0_REDIRECT_URI,
        "scope": "openid profile email",
        "audience": f"https://{AUTH0_DOMAIN}/api/v2/",
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    }
    query_string = urllib.parse.urlencode(params)
    authorization_url = f"https://{AUTH0_DOMAIN}/authorize?{query_string}"
    return authorization_url, code_verifier


def exchange_pkce_code_for_tokens(code: str, code_verifier: str):
    import requests  # Imported locally to avoid circular dependency in a multi-file setup

    if not all([AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_REDIRECT_URI]):
        raise ValueError("Missing Auth0 environment variables")

    token_url = f"https://{AUTH0_DOMAIN}/oauth/token"
    headers = {"content-type": "application/x-www-form-urlencoded"}
    payload = {
        "grant_type": "authorization_code",
        "client_id": AUTH0_CLIENT_ID,
        "code": code,
        "redirect_uri": AUTH0_REDIRECT_URI,
        "code_verifier": code_verifier,
    }

    response = requests.post(token_url, headers=headers, data=payload)
    response.raise_for_status()
    return response.json()
