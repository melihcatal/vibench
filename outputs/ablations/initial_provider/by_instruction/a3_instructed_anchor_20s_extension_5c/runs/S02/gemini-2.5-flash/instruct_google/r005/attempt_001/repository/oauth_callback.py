import os
from google_auth_oauthlib.flow import Flow

def handle_oauth_callback(authorization_response_url, state):
    """
    Handles the OAuth 2.0 callback, exchanges the authorization code for tokens.
    """
    client_id = os.environ.get("GOOGLE_CLIENT_ID")
    client_secret = os.environ.get("GOOGLE_CLIENT_SECRET")
    redirect_uri = os.environ.get("GOOGLE_REDIRECT_URI", "http://localhost:8080/oauth2callback")

    flow = Flow.from_client_config(
        client_config={
            "web": {
                "client_id": client_id,
                "client_secret": client_secret,
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

    flow.fetch_token(authorization_response=authorization_response_url)

    credentials = flow.credentials
    print("Successfully exchanged authorization code for tokens.")
    print(f"Access Token: {credentials.token}")
    print(f"Refresh Token: {credentials.refresh_token}")
    print(f"ID Token: {credentials.id_token}")

    return credentials
