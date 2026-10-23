import os
import urllib.parse

# Google Identity Platform OAuth 2.0
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "YOUR_GOOGLE_CLIENT_ID")
GOOGLE_REDIRECT_URI = os.environ.get("GOOGLE_REDIRECT_URI", "http://localhost:8000/oauth_callback")
GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
SCOPE = "openid profile email"

def generate_google_auth_url():
    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": SCOPE,
        "access_type": "offline",
        "prompt": "select_account"
    }
    return f"{GOOGLE_AUTH_URL}?{urllib.parse.urlencode(params)}"

if __name__ == "__main__":
    auth_url = generate_google_auth_url()
    print(f"Please visit this URL to start Google OAuth login:\n{auth_url}")
