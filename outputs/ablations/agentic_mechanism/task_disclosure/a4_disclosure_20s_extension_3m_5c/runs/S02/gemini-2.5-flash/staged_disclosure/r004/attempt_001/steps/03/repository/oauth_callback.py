
import os
import requests
from flask import Flask, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = os.urandom(24) # A secret key for session management

# Google OAuth2 Configuration
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.environ.get("GOOGLE_REDIRECT_URI") # This should be the URL of your callback endpoint

@app.route("/oauth/callback")
def oauth_callback():
    code = request.args.get("code")
    if not code:
        return "Error: Authorization code not found.", 400

    token_url = "https://oauth2.googleapis.com/token"
    payload = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }

    try:
        response = requests.post(token_url, data=payload)
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        tokens = response.json()

        # In a real application, you would save these tokens securely
        # and use them to access user data from Google APIs.
        session["google_access_token"] = tokens.get("access_token")
        session["google_refresh_token"] = tokens.get("refresh_token") # May not be present depending on scope

        return f"Successfully exchanged code for tokens: {tokens}"
    except requests.exceptions.RequestException as e:
        return f"Error exchanging code for tokens: {e}", 500

@app.route("/")
def index():
    # Example of how to initiate the Google OAuth flow
    # In a real app, you'd have a button or link for "Login with Google"
    auth_url = (
        "https://accounts.google.com/o/oauth2/auth?"
        f"client_id={GOOGLE_CLIENT_ID}&"
        "response_type=code&"
        f"redirect_uri={GOOGLE_REDIRECT_URI}&"
        "scope=openid%20profile%20email&" # Scopes for user info
        "access_type=offline&" # To get a refresh token
        "prompt=consent" # To always show the consent screen
    )
    return f'<h1>Welcome!</h1><p><a href="{auth_url}">Login with Google</a></p>'

if __name__ == "__main__":
    # Ensure environment variables are set for client ID, client secret, and redirect URI
    if not all([GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REDIRECT_URI]):
        print("Error: Please set GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, and GOOGLE_REDIRECT_URI environment variables.")
        print("Example: export GOOGLE_CLIENT_ID='YOUR_CLIENT_ID'")
        print("Example: export GOOGLE_CLIENT_SECRET='YOUR_CLIENT_SECRET'")
        print("Example: export GOOGLE_REDIRECT_URI='http://127.0.0.1:5000/oauth/callback'")
        exit(1)
    app.run(debug=True)
