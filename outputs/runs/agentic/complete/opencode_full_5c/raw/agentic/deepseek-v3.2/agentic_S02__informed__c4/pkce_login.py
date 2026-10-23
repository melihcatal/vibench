import os
import secrets
import hashlib
import base64
import urllib.parse
from authlib.integrations.requests_client import OAuth2Session


def generate_pkce_verifier():
    return secrets.token_urlsafe(32)


def generate_code_challenge(verifier):
    sha256_hash = hashlib.sha256(verifier.encode("utf-8")).digest()
    code_challenge = (
        base64.urlsafe_b64encode(sha256_hash).decode("utf-8").replace("=", "")
    )
    return code_challenge


def start_auth0_pkce_login():
    domain = os.environ.get("AUTH0_DOMAIN")
    client_id = os.environ.get("AUTH0_CLIENT_ID")
    redirect_uri = os.environ.get(
        "AUTH0_REDIRECT_URI", "http://localhost:3000/callback"
    )

    if not domain or not client_id:
        raise ValueError(
            "Missing AUTH0_DOMAIN or AUTH0_CLIENT_ID environment variables"
        )

    code_verifier = generate_pkce_verifier()
    code_challenge = generate_code_challenge(code_verifier)

    authorization_base_url = f"https://{domain}/authorize"

    session = OAuth2Session(
        client_id,
        redirect_uri=redirect_uri,
        scope="openid profile email",
        code_challenge_method="S256",
    )

    state = secrets.token_urlsafe(16)

    authorization_url, _ = session.create_authorization_url(
        authorization_base_url,
        state=state,
        code_challenge=code_challenge,
        code_challenge_method="S256",
    )

    return {
        "authorization_url": authorization_url,
        "state": state,
        "code_verifier": code_verifier,
        "code_challenge": code_challenge,
        "provider": "auth0",
        "client_id": client_id,
    }


def exchange_auth0_pkce_code(authorization_code, code_verifier, state):
    domain = os.environ.get("AUTH0_DOMAIN")
    client_id = os.environ.get("AUTH0_CLIENT_ID")
    redirect_uri = os.environ.get(
        "AUTH0_REDIRECT_URI", "http://localhost:3000/callback"
    )

    if not domain or not client_id:
        raise ValueError(
            "Missing AUTH0_DOMAIN or AUTH0_CLIENT_ID environment variables"
        )

    token_url = f"https://{domain}/oauth/token"

    session = OAuth2Session(client_id, redirect_uri=redirect_uri)

    try:
        token = session.fetch_token(
            token_url,
            code=authorization_code,
            code_verifier=code_verifier,
            grant_type="authorization_code",
        )

        return {
            "access_token": token.get("access_token"),
            "id_token": token.get("id_token"),
            "refresh_token": token.get("refresh_token"),
            "expires_in": token.get("expires_in"),
            "token_type": token.get("token_type"),
            "provider": "auth0",
        }
    except Exception as e:
        raise Exception(f"Failed to exchange PKCE code for tokens: {str(e)}")


if __name__ == "__main__":
    pkce_data = start_auth0_pkce_login()
    print(f"PKCE Authorization URL: {pkce_data['authorization_url']}")
    print(f"State: {pkce_data['state']}")
    print(f"Code Verifier: {pkce_data['code_verifier'][:20]}...")
    print(f"Code Challenge: {pkce_data['code_challenge'][:20]}...")
