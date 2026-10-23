import os
from urllib.parse import urlencode

# Google Identity Platform (OAuth 2.0)
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "YOUR_GOOGLE_CLIENT_ID")
GOOGLE_REDIRECT_URI = os.environ.get("GOOGLE_REDIRECT_URI", "http://localhost:8080/oauth/callback/google")
GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"

def get_google_auth_url():
    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "consent",
    }
    return f"{GOOGLE_AUTH_URL}?{urlencode(params)}"

if __name__ == "__main__":
    print(f"Navigate to this URL to start Google OAuth login: {get_google_auth_url()}")
