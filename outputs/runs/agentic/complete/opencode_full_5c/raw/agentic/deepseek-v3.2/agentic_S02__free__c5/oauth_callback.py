import os
from authlib.integrations.requests_client import OAuth2Session


def handle_oauth_callback(authorization_response, state, code_verifier):
    client_id = os.environ.get("GOOGLE_OAUTH_CLIENT_ID")
    client_secret = os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET")
    redirect_uri = os.environ.get(
        "GOOGLE_OAUTH_REDIRECT_URI", "http://localhost:8000/callback"
    )

    token_endpoint = "https://oauth2.googleapis.com/token"

    session = OAuth2Session(
        client_id, client_secret, redirect_uri=redirect_uri, state=state
    )

    token = session.fetch_token(
        token_endpoint,
        authorization_response=authorization_response,
        code_verifier=code_verifier,
    )

    return {
        "access_token": token.get("access_token"),
        "refresh_token": token.get("refresh_token"),
        "id_token": token.get("id_token"),
        "expires_in": token.get("expires_in"),
        "token_type": token.get("token_type"),
        "provider": "google",
    }
