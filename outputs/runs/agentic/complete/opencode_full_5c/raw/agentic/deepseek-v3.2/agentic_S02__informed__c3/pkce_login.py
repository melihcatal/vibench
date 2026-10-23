import os
import secrets
import hashlib
import base64
import urllib.parse
import requests


def generate_pkce_verifier():
    verifier = (
        base64.urlsafe_b64encode(secrets.token_bytes(32)).rstrip(b"=").decode("utf-8")
    )
    return verifier


def generate_pkce_challenge(verifier):
    challenge = hashlib.sha256(verifier.encode("utf-8")).digest()
    challenge_b64 = base64.urlsafe_b64encode(challenge).rstrip(b"=").decode("utf-8")
    return challenge_b64


def start_pkce_login():
    domain = os.environ.get("AUTH0_DOMAIN")
    client_id = os.environ.get("AUTH0_CLIENT_ID")
    redirect_uri = os.environ.get(
        "AUTH0_CALLBACK_URL", "http://localhost:3000/callback"
    )

    if not domain or not client_id:
        raise ValueError(
            "AUTH0_DOMAIN and AUTH0_CLIENT_ID environment variables are required"
        )

    verifier = generate_pkce_verifier()
    challenge = generate_pkce_challenge(verifier)
    state = secrets.token_urlsafe(32)
    nonce = secrets.token_urlsafe(32)

    auth_url = f"https://{domain}/authorize"
    params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": "openid profile email",
        "state": state,
        "nonce": nonce,
        "code_challenge": challenge,
        "code_challenge_method": "S256",
    }

    full_url = f"{auth_url}?{urllib.parse.urlencode(params)}"

    return {
        "auth_url": full_url,
        "state": state,
        "nonce": nonce,
        "code_verifier": verifier,
    }


def exchange_pkce_code(auth_code, code_verifier, state, stored_state):
    if state != stored_state:
        raise ValueError("State mismatch - possible CSRF attack")

    domain = os.environ.get("AUTH0_DOMAIN")
    client_id = os.environ.get("AUTH0_CLIENT_ID")
    redirect_uri = os.environ.get(
        "AUTH0_CALLBACK_URL", "http://localhost:3000/callback"
    )

    if not all([domain, client_id]):
        raise ValueError("Missing Auth0 configuration")

    token_url = f"https://{domain}/oauth/token"

    payload = {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "code_verifier": code_verifier,
        "code": auth_code,
        "redirect_uri": redirect_uri,
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    response = requests.post(token_url, data=payload, headers=headers)

    if response.status_code != 200:
        raise Exception(f"PKCE token exchange failed: {response.text}")

    token_data = response.json()

    return {
        "id_token": token_data.get("id_token"),
        "access_token": token_data.get("access_token"),
        "refresh_token": token_data.get("refresh_token"),
        "expires_in": token_data.get("expires_in"),
        "token_type": token_data.get("token_type"),
    }


def handle_pkce_login():
    try:
        pkce_data = start_pkce_login()
        print(f"Redirect user to: {pkce_data['auth_url']}")
        return pkce_data
    except Exception as e:
        print(f"Error starting PKCE login: {e}")
        raise
