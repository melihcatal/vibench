\
import os\n\
import urllib.parse\n\
\n\
# Google OAuth 2.0 Configuration\n\
GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/auth"\n\
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token" # Not used in this "start login" example, but good to have.\n\
\n\
# Replace with your actual Google OAuth client ID\n\
# You can get this from the Google Cloud Console: APIs & Services -> Credentials\n\
CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "YOUR_GOOGLE_CLIENT_ID")\n\
\n\
# Replace with your actual redirect URI\n\
# This must be registered in your Google Cloud Console for the OAuth client ID\n\
REDIRECT_URI = os.environ.get("GOOGLE_REDIRECT_URI", "http://localhost:8080/callback")\n\
\n\
# Scopes define the level of access you are requesting.\n\
# For example, "openid email profile" requests access to the user\'s ID, email, and basic profile information.\n\
SCOPES = ["openid", "email", "profile"]\n\
\n\
def start_oauth_login():\n\
    """\n\
    Constructs and prints the Google OAuth authorization URL.\n\
    The user needs to open this URL in their browser to initiate the login process.\n\
    """\n\
    params = {\n\
        "client_id": CLIENT_ID,\n\
        "redirect_uri": REDIRECT_URI,\n\
        "response_type": "code",\n\
        "scope": " ".join(SCOPES),\n\
        "access_type": "offline",  # To get a refresh token for long-lived access\n\
        "prompt": "consent",  # To ensure the consent screen is shown even if already authorized\n\
    }\n\
    \n\
    authorization_url = f"{GOOGLE_AUTH_URL}?{urllib.parse.urlencode(params)}"\n\
    print(f"Please open the following URL in your browser to start the Google OAuth login:\\n{authorization_url}")\n\
\n\
if __name__ == "__main__":\n\
    start_oauth_login()\n\
