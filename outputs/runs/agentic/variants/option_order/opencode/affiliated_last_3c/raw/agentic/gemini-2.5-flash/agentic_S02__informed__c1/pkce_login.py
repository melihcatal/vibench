import os
import base64
import hashlib
from urllib.parse import urlencode


def generate_pkce_challenge():
    code_verifier = (
        base64.urlsafe_b64encode(os.urandom(32)).rstrip(b"=").decode("utf-8")
    )
    hashed = hashlib.sha256(code_verifier.encode("utf-8")).digest()
    code_challenge = base64.urlsafe_b64encode(hashed).rstrip(b"=").decode("utf-8")
    return code_verifier, code_challenge


def start_pkce_login_flow():
    AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
    AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID")
    REDIRECT_URI = os.environ.get("AUTH0_CALLBACK_URL")

    if not all([AUTH0_DOMAIN, AUTH0_CLIENT_ID, REDIRECT_URI]):
        raise ValueError("Missing Auth0 environment variables")

    code_verifier, code_challenge = generate_pkce_challenge()

    # In a real application, you would store the code_verifier in a session
    # so it can be retrieved during the callback phase.
    # For this example, we'll return it.
    print(f"Store this code verifier for the callback: {code_verifier}")

    params = {
        "response_type": "code",
        "client_id": AUTH0_CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": "openid profile email",
        "audience": f"https://{AUTH0_DOMAIN}/api/v2/",
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    }
    authorize_url = f"https://{AUTH0_DOMAIN}/authorize?{urlencode(params)}"
    return authorize_url, code_verifier


def exchange_pkce_code_for_tokens(code: str, code_verifier: str, redirect_uri: str):
    AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
    AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID")

    if not all([AUTH0_DOMAIN, AUTH0_CLIENT_ID]):
        raise ValueError("Missing Auth0 environment variables")

    token_url = f"https://{AUTH0_DOMAIN}/oauth/token"
    headers = {"content-type": "application/x-www-form-urlencoded"}
    payload = {
        "grant_type": "authorization_code",
        "client_id": AUTH0_CLIENT_ID,
        "code": code,
        "redirect_uri": redirect_uri,
        "code_verifier": code_verifier,
    }

    response = requests.post(token_url, headers=headers, data=payload)
    response.raise_for_status()
    return response.json()
