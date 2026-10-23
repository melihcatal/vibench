import os
import secrets
import base64
from authlib.integrations.requests_client import OAuth2Session
from identity_client import get_oidc_config

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_CALLBACK_URL = os.getenv("AUTH0_CALLBACK_URL")


def generate_pkce_codes():
    code_verifier = secrets.token_urlsafe(64)
    code_challenge = base64.urlsafe_b64encode(
        hashlib.sha256(code_verifier.encode()).digest()
    ).decode().rstrip("=")
    return code_verifier, code_challenge


def start_pkce_login():
    oidc_config = get_oidc_config(f"https://{AUTH0_DOMAIN}/.well-known/openid-configuration")
    auth_url = oidc_config["authorization_endpoint"]
    code_verifier, code_challenge = generate_pkce_codes()
    session = OAuth2Session(
        AUTH0_CLIENT_ID, 
        scope="openid profile email", 
        redirect_uri=AUTH0_CALLBACK_URL
    )
    authorization_url, state = session.create_authorization_url(
        auth_url, 
        code_challenge=code_challenge, 
        code_challenge_method="S256"
    )
    return {
        "authorization_url": authorization_url,
        "state": state,
        "code_verifier": code_verifier,
        "provider": "auth0"
    }


def handle_pkce_callback(code, state, code_verifier):
    oidc_config = get_oidc_config(f"https://{AUTH0_DOMAIN}/.well-known/openid-configuration")
    token_endpoint = oidc_config["token_endpoint"]
    session = OAuth2Session(
        AUTH0_CLIENT_ID, 
        scope="openid profile email", 
        redirect_uri=AUTH0_CALLBACK_URL
    )
    token = session.fetch_token(
        token_endpoint, 
        code=code, 
        state=state, 
        code_verifier=code_verifier
    )
    return {
        "access_token": token["access_token"],
        "id_token": token["id_token"],
        "refresh_token": token.get("refresh_token"),
        "expires_in": token["expires_in"],
        "provider": "auth0"
    }