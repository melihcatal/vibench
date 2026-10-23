import os
from google_auth_oauthlib.flow import Flow
from oauthlib.oauth2 import WebApplicationClient
import base64
import hashlib

def start_pkce_login():
    """
    Starts an OAuth 2.0 authorization code flow with PKCE for public clients.
    """
    client_id = os.environ.get("GOOGLE_CLIENT_ID")
    redirect_uri = os.environ.get("GOOGLE_REDIRECT_URI", "http://localhost:8080/oauth2callback")

    # Generate a code verifier
    code_verifier = base64.urlsafe_b64encode(os.urandom(32)).rstrip(b'=').decode('utf-8')

    # Hash the code verifier to create the code challenge
    code_challenge_bytes = hashlib.sha256(code_verifier.encode('utf-8')).digest()
    code_challenge = base64.urlsafe_b64encode(code_challenge_bytes).rstrip(b'=').decode('utf-8')

    flow = Flow.from_client_config(
        client_config={
            "web": {
                "client_id": client_id,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [redirect_uri],
                "scopes": [
                    "https://www.googleapis.com/auth/userinfo.email",
                    "https://www.googleapis.com/auth/userinfo.profile",
                    "openid"
                ]
            }
        },
        scopes=[
            "https://www.googleapis.com/auth/userinfo.email",
            "https://www.googleapis.com/auth/userinfo.profile",
            "openid"
        ],
        redirect_uri=redirect_uri
    )

    authorization_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        code_challenge=code_challenge,
        code_challenge_method="S256"
    )

    print(f"Please go to this URL to authorize (PKCE): {authorization_url}")
    print(f"State parameter: {state}")
    print(f"Code Verifier (to be stored securely): {code_verifier}")

    return authorization_url, state, code_verifier

def handle_pkce_callback(authorization_response_url, state, code_verifier):
    """
    Handles the OAuth 2.0 callback for PKCE, exchanges the authorization code for tokens.
    """
    client_id = os.environ.get("GOOGLE_CLIENT_ID")
    redirect_uri = os.environ.get("GOOGLE_REDIRECT_URI", "http://localhost:8080/oauth2callback")

    flow = Flow.from_client_config(
        client_config={
            "web": {
                "client_id": client_id,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [redirect_uri],
                "scopes": [
                    "https://www.googleapis.com/auth/userinfo.email",
                    "https://www.googleapis.com/auth/userinfo.profile",
                    "openid"
                ]
            }
        },
        scopes=[
            "https://www.googleapis.com/auth/userinfo.email",
            "https://www.googleapis.com/auth/userinfo.profile",
            "openid"
        ],
        redirect_uri=redirect_uri,
        state=state
    )

    flow.fetch_token(authorization_response=authorization_response_url, code_verifier=code_verifier)

    credentials = flow.credentials
    print("Successfully exchanged authorization code for tokens (PKCE).")
    print(f"Access Token: {credentials.token}")
    print(f"Refresh Token: {credentials.refresh_token}")
    print(f"ID Token: {credentials.id_token}")

    return credentials
