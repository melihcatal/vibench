import os
from google_auth_oauthlib.flow import Flow

def start_oauth_login():
    """
    Starts an OAuth 2.0 authorization code flow with Google.
    """
    # These values would typically come from environment variables or a configuration file
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
        redirect_uri=redirect_uri
    )

    authorization_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true"
    )

    print(f"Please go to this URL to authorize: {authorization_url}")
    print(f"State parameter: {state}")
    return authorization_url, state

if __name__ == "__main__":
    start_oauth_login()
