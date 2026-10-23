import os
from flask import Flask, redirect, url_for, session, request
from google_auth_oauthlib.flow import Flow
import google.auth.transport.requests

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "supersecret")

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
GOOGLE_AUTH_URI = "https://accounts.google.com/o/oauth2/auth"
GOOGLE_TOKEN_URI = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URI = "https://openidconnect.googleapis.com/v1/userinfo"
REDIRECT_URI = "http://localhost:5000/oauth2callback"
SCOPES = ["openid", "https://www.googleapis.com/auth/userinfo.email", "https://www.googleapis.com/auth/userinfo.profile"]

def handle_google_oauth_callback():
    state = session["state"]

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
        state=state,
        redirect_uri=REDIRECT_URI
    )

    flow.fetch_token(authorization_response=request.url)

    credentials = flow.credentials
    session["credentials"] = {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes,
    }

    return "Successfully logged in with Google!"

if __name__ == "__main__":
    # This is a minimal example and not a production-ready server.
    # In a real application, this would be a Flask route.
    # For demonstration, assume a request context and a 'state' in session.
    with app.test_request_context('/oauth2callback?state=mock_state&code=mock_code'):
        session['state'] = 'mock_state'
        print(handle_google_oauth_callback())
