
import os
from flask import Flask, redirect, url_for, request, session
from google_auth_oauthlib.flow import Flow
import google.oauth2.credentials

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "supersecret")

# Configuration for Google OAuth
# These should ideally come from environment variables or a config file
CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "YOUR_GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", "YOUR_GOOGLE_CLIENT_SECRET")
REDIRECT_URI = os.environ.get("GOOGLE_REDIRECT_URI", "http://localhost:5000/oauth2callback")
SCOPES = ["https://www.googleapis.com/auth/userinfo.email", "https://www.googleapis.com/auth/userinfo.profile", "openid"]

@app.route("/authorize")
def authorize():
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
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

@app.route("/oauth2callback")
def oauth2callback():
    state = session["state"]
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [REDIRECT_URI],
                "scopes": SCOPES,
            }
        },
        scopes=SCOPES,
        state=state,
        redirect_uri=REDIRECT_URI
    )

    try:
        flow.fetch_token(authorization_response=request.url)
    except Exception as e:
        return f"Error exchanging code for tokens: {e}", 500

    credentials = flow.credentials
    session["credentials"] = {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes,
    }

    # You can now use credentials to access Google APIs
    return "Successfully obtained tokens!"

@app.route("/")
def index():
    if "credentials" not in session:
        return "<p>You are not logged in. <a href='/authorize'>Login with Google</a></p>"
    else:
        return "<p>You are logged in!</p>"

if __name__ == "__main__":
    # In a real application, you would configure Flask to run in production mode
    # and use a proper WSGI server (e.g., Gunicorn, uWSGI).
    # For local development, ensure GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET,
    # GOOGLE_REDIRECT_URI, and FLASK_SECRET_KEY are set in your environment.
    app.run(debug=True, port=5000)
