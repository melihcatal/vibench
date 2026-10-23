import os

def get_google_oauth_client_config():
    """
    Returns a dictionary containing Google OAuth client configuration.
    """
    return {
        "client_id": os.environ.get("GOOGLE_CLIENT_ID"),
        "client_secret": os.environ.get("GOOGLE_CLIENT_SECRET"),
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "redirect_uris": [os.environ.get("GOOGLE_REDIRECT_URI", "http://localhost:8080/oauth2callback")],
        "scopes": [
            "https://www.googleapis.com/auth/userinfo.email",
            "https://www.googleapis.com/auth/userinfo.profile",
            "openid"
        ]
    }
