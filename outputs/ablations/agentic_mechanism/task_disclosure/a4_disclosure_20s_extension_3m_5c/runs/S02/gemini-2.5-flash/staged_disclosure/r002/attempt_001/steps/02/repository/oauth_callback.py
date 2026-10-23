import os
from flask import Flask, request, redirect, url_for, session
from google.oauth2 import credentials
import google.auth.transport.requests

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Load client ID and client secret from environment variables
CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = "http://localhost:5000/oauth_callback" # This should match your Google Cloud Console setting

@app.route("/")
def index():
    if "credentials" not in session:
        # Redirect to Google's OAuth consent screen
        auth_uri = (
            "https://accounts.google.com/o/oauth2/auth?"
            "response_type=code&"
            "client_id={}&"
            "redirect_uri={}&"
            "scope=openid%20profile%20email&"
            "access_type=offline".format(CLIENT_ID, REDIRECT_URI)
        )
        return redirect(auth_uri)
    else:
        # User is already authenticated
        return "You are authenticated!"

@app.route("/oauth_callback")
def oauth_callback():
    code = request.args.get("code")
    if not code:
        return "Authorization code not found.", 400

    try:
        # Exchange authorization code for tokens
        flow = credentials.InstalledAppFlow.from_client_config(
            {
                "web": {
                    "client_id": CLIENT_ID,
                    "client_secret": CLIENT_SECRET,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": [REDIRECT_URI],
                }
            },
            scopes=["openid", "profile", "email"],
        )
        flow.redirect_uri = REDIRECT_URI
        flow.fetch_token(code=code)

        creds = flow.credentials
        session["credentials"] = {
            "token": creds.token,
            "refresh_token": creds.refresh_token,
            "token_uri": creds.token_uri,
            "client_id": creds.client_id,
            "client_secret": creds.client_secret,
            "scopes": creds.scopes,
        }

        return f"Access Token: {creds.token}<br>Refresh Token: {creds.refresh_token}"
    except Exception as e:
        return f"Error during token exchange: {e}", 500

if __name__ == "__main__":
    # For local development, set these environment variables:
    # export GOOGLE_CLIENT_ID="YOUR_CLIENT_ID"
    # export GOOGLE_CLIENT_SECRET="YOUR_CLIENT_SECRET"
    app.run(debug=True)
