from authlib.integrations.requests_client import OAuth2Session
import os

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN", "https://example.auth0.com")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_CALLBACK_URL = os.getenv("AUTH0_CALLBACK_URL", "http://localhost:5000/callback")


def start_auth0_pkce_login():
    session = OAuth2Session(
        AUTH0_CLIENT_ID,
        scope="openid profile email",
        redirect_uri=AUTH0_CALLBACK_URL
    )
    authorization_url, state = session.create_authorization_url(
        f"{AUTH0_DOMAIN}/authorize",
        code_verifier=session.generate_code_verifier()
    )
    return {
        "authorization_url": authorization_url,
        "state": state,
        "code_verifier": session.code_verifier,
        "provider": "auth0"
    }


def handle_auth0_pkce_callback(code, code_verifier, state):
    session = OAuth2Session(
        AUTH0_CLIENT_ID,
        scope="openid profile email",
        redirect_uri=AUTH0_CALLBACK_URL,
        state=state,
        code_verifier=code_verifier
    )
    token = session.fetch_token(
        f"{AUTH0_DOMAIN}/oauth/token",
        code=code,
        grant_type="authorization_code"
    )
    return {
        "token": token,
        "provider": "auth0"
    }