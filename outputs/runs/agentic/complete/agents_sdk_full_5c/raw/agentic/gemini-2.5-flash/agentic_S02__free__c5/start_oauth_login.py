import os
import urllib.parse

# Replace with your actual client ID and redirect URI
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "YOUR_GOOGLE_CLIENT_ID")
REDIRECT_URI = os.environ.get("REDIRECT_URI", "http://localhost:8000/oauth_callback")
SCOPES = "openid profile email"

def generate_google_auth_url():
    """Generates the Google OAuth 2.0 authorization URL."""
    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": SCOPES,
        "access_type": "offline",
        "prompt": "select_account",
    }
    query_string = urllib.parse.urlencode(params)
    return f"https://accounts.google.com/o/oauth2/v2/auth?{query_string}"

if __name__ == "__main__":
    auth_url = generate_google_auth_url()
    print(f"Please visit this URL to start the Google OAuth login flow:\n{auth_url}")
