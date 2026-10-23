import os
from flask import Flask, redirect, url_for, session, request
from google_auth_oauthlib.flow import Flow

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "supersecret")

# Google OAuth 2.0 configuration
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
GOOGLE_AUTH_URI = "https://accounts.google.com/o/oauth2/auth"
GOOGLE_TOKEN_URI = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URI = "https://openidconnect.googleapis.com/v1/userinfo"
REDIRECT_URI = "http://localhost:5000/oauth2callback"
SCOPES = ["openid", "https://www.googleapis.com/auth/userinfo.email", "https://www.googleapis.com/auth/userinfo.profile"]

def start_google_oauth_login():
    flow = Flow.from_client_config(
        client_config={
            "web": {
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "auth_uri": GOOGLE_AUTH_URI,
                "token_uri": GOOGLE_TOKEN_URI,
                "userinfo_uri": GOOGLE_USERINFO_URI,
                "redirect_uris": [REDIRECT_URI],
                "scopes": SCOPES,
            }
        },
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )

    authorization_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true"
    )

    session["state"] = state
    return redirect(authorization_url)

if __name__ == "__main__":
    # This is a minimal example and not a production-ready server.
    # In a real application, you would integrate this into your Flask app routes.
    # For demonstration purposes, you can run this file directly to test the redirect.
    with app.test_request_context():
        print(start_google_oauth_login().headers["Location"])
