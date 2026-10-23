
import os
import urllib.parse

# Google OAuth 2.0 Configuration
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "YOUR_GOOGLE_CLIENT_ID")
GOOGLE_REDIRECT_URI = os.environ.get("GOOGLE_REDIRECT_URI", "http://localhost:8000/callback")

# Scopes for Google (e.g., profile and email)
GOOGLE_SCOPES = [
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/userinfo.email"
]

# Google Authorization Endpoint
GOOGLE_AUTHORIZATION_BASE_URL = "https://accounts.google.com/o/oauth2/v2/auth"

def start_google_oauth_login():
    """
    Constructs and prints the Google OAuth authorization URL.
    """
    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": " ".join(GOOGLE_SCOPES),
        "access_type": "offline",  # To get a refresh token
        "prompt": "consent"       # To ensure refresh token is always returned
    }
    
    authorization_url = f"{GOOGLE_AUTHORIZATION_BASE_URL}?{urllib.parse.urlencode(params)}"
    print(f"Please visit this URL to authorize with Google:\n{authorization_url}")

if __name__ == "__main__":
    start_google_oauth_login()
