import requests
import urllib.parse
import identity_client

# Configuration (Google Identity Platform used as concrete provider)
CLIENT_ID = "YOUR_GOOGLE_CLIENT_ID"
REDIRECT_URI = "http://localhost:5000/oauth_callback"
SCOPES = ["openid", "email", "profile"]
AUTHORIZATION_ENDPOINT = "https://accounts.google.com/o/oauth2/v2/auth"

def start_oauth_login():
    # Generate PKCE code verifier and challenge (handled in pkce_login)
    # Build authorization URL
    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": " ".join(SCOPES),
        "prompt": "consent",
        "access_type": "offline",
        "include_granted_scopes": "true",
    }
    url = AUTHORIZATION_ENDPOINT + "?" + urllib.parse.urlencode(params)
    print("Redirect user to:", url)
    # In a real web app, you would return an HTTP redirect
    return url

if __name__ == "__main__":
    start_oauth_login()
