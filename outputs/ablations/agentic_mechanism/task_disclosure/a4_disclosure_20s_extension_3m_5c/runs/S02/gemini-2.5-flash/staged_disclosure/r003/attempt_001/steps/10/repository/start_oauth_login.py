
import os

# Google OAuth 2.0 Endpoints
AUTHORIZATION_BASE_URL = "https://accounts.google.com/o/oauth2/v2/auth"

# Replace with your actual client ID and redirect URI from Google Cloud Console
CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "YOUR_GOOGLE_CLIENT_ID")
REDIRECT_URI = os.environ.get("GOOGLE_REDIRECT_URI", "http://localhost:8080/callback")

# Scopes define the permissions your application requests
SCOPE = "openid email profile"

def start_google_oauth_login():
    """
    Constructs and prints the Google OAuth authorization URL.
    The user should open this URL in their browser to initiate the login process.
    """
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": SCOPE,
        "access_type": "offline",  # Request a refresh token
        "prompt": "consent",      # Force consent screen
    }

    import urllib.parse
    query_string = urllib.parse.urlencode(params)
    authorization_url = f"{AUTHORIZATION_BASE_URL}?{query_string}"

    print(f"Please open the following URL in your browser to start Google OAuth login:")
    print(authorization_url)
    print("\nNote: For a real application, you would need a web server running at")
    print(f"'{REDIRECT_URI}' to handle the redirect and exchange the authorization code for tokens.")

if __name__ == "__main__":
    start_google_oauth_login()
