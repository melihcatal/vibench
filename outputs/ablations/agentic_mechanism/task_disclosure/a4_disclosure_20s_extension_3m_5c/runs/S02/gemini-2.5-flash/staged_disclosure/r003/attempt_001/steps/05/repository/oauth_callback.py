
import os
from flask import Flask, redirect, url_for, session, request
from google_auth_oauthlib.flow import Flow
import google.oauth2.credentials

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Replace with your Google API client ID and client secret
CLIENT_SECRETS_FILE = "client_secret.json" # You would typically load this from a file or environment variables
# For demonstration, let's assume a simplified client_secret.json structure for clarity
# In a real application, you'd have a proper client_secret.json file downloaded from Google Cloud Console.

# Dummy values for demonstration purposes, replace with your actual values
CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "YOUR_GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", "YOUR_GOOGLE_CLIENT_SECRET")
REDIRECT_URI = os.environ.get("GOOGLE_REDIRECT_URI", "http://localhost:5000/oauth_callback")

SCOPES = ['https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile']

@app.route("/authorize")
def authorize():
    flow = Flow.from_client_config(
        client_config={
            "web": {
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [REDIRECT_URI]
            }
        },
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )

    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )

    session['oauth_state'] = state
    return redirect(authorization_url)

@app.route("/oauth_callback")
def oauth_callback():
    state = session.pop('oauth_state', None)

    flow = Flow.from_client_config(
        client_config={
            "web": {
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [REDIRECT_URI]
            }
        },
        scopes=SCOPES,
        state=state,
        redirect_uri=REDIRECT_URI
    )

    try:
        flow.fetch_token(authorization_response=request.url)
        credentials = flow.credentials
        session['credentials'] = {
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes
        }
        return "Authentication successful! Tokens stored in session."
    except Exception as e:
        return f"Authentication failed: {e}"

@app.route("/")
def index():
    if 'credentials' not in session:
        return '<p>You are not logged in. <a href="/authorize">Log in with Google</a></p>'
    return '<p>Logged in. <a href="/logout">Log out</a></p>'

@app.route("/logout")
def logout():
    session.pop('credentials', None)
    return redirect(url_for('index'))

if __name__ == "__main__":
    # Ensure you have set GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, and GOOGLE_REDIRECT_URI
    # in your environment variables or replace the dummy values above.
    # For local testing, you might need to install flask and google-auth-oauthlib:
    # pip install Flask google-auth-oauthlib google-api-python-client
    app.run(debug=True)
