import os
import urllib.parse
import uuid

# Google OAuth 2.0 configuration
GOOGLE_AUTHORIZATION_BASE_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_SCOPES = [
    "openid",
    "email",
    "profile",
]

def start_google_oauth_login():
    """
    Starts an OAuth or OIDC authorization-code login flow with Google.
    """
    client_id = os.environ.get("GOOGLE_CLIENT_ID")
    redirect_uri = os.environ.get("GOOGLE_REDIRECT_URI")

    if not client_id or not redirect_uri:
        raise ValueError("GOOGLE_CLIENT_ID and GOOGLE_REDIRECT_URI environment variables must be set.")

    state = str(uuid.uuid4()) # Generate a unique state parameter for security

    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": " ".join(GOOGLE_SCOPES),
        "response_type": "code",
        "access_type": "offline",
        "prompt": "select_account",
        "state": state,
    }

    authorization_url = f"{GOOGLE_AUTHORIZATION_BASE_URL}?{urllib.parse.urlencode(params)}"
    return authorization_url

if __name__ == "__main__":
    # Example usage (in a real application, you would redirect the user to this URL)
    try:
        login_url = start_google_oauth_login()
        print(f"Please visit this URL to log in: {login_url}")
    except ValueError as e:
        print(f"Error: {e}")
