
import os
import urllib.parse

# Google OAuth 2.0 Authorization Endpoint
GOOGLE_AUTHORIZATION_BASE_URL = "https://accounts.google.com/o/oauth2/v2/auth"

# Client ID and Redirect URI (these would typically be loaded from environment variables or a config file)
CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "YOUR_GOOGLE_CLIENT_ID")
REDIRECT_URI = os.environ.get("GOOGLE_REDIRECT_URI", "http://localhost:8000/oauth_callback")
SCOPE = "openid profile email"  # OIDC scopes
RESPONSE_TYPE = "code"

def start_oauth_login():
    """
    Constructs the Google OAuth 2.0 authorization URL and returns it.
    In a real application, you would redirect the user to this URL.
    """
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPE,
        "response_type": RESPONSE_TYPE,
        "access_type": "offline",  # Request a refresh token
        "prompt": "consent",       # Force consent screen
    }
    authorization_url = f"{GOOGLE_AUTHORIZATION_BASE_URL}?{urllib.parse.urlencode(params)}"
    return authorization_url

if __name__ == "__main__":
    login_url = start_oauth_login()
    print(f"Please visit this URL to start the OAuth login process:\n{login_url}")
