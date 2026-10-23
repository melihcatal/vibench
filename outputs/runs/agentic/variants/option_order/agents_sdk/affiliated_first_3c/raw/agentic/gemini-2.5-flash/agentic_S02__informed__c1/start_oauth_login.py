import os
from flask import Flask, redirect, url_for, session
import google.auth.transport.requests
from google_auth_oauthlib.flow import Flow

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "supersecretkey")

# Configuration for Google Identity Platform OIDC
# Replace with your client ID, client secret, and redirect URI
CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = os.environ.get("GOOGLE_REDIRECT_URI", "http://localhost:5000/oauth2callback")

# Scopes for Google Identity Platform
SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
]

@app.route("/login")
def login():
    flow = Flow.from_client_secrets_file(
        "client_secret.json",  # This file contains client_id and client_secret
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )

    flow.redirect_uri = REDIRECT_URI

    authorization_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true"
    )

    session["state"] = state
    return redirect(authorization_url)

if __name__ == "__main__":
    # Create a dummy client_secret.json for demonstration if not present
    if not os.path.exists("client_secret.json"):
        with open("client_secret.json", "w") as f:
            f.write(f'''{
                "web": {
                    "client_id": "{CLIENT_ID}",
                    "project_id": "your-project-id",
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                    "client_secret": "{CLIENT_SECRET}",
                    "redirect_uris": ["{REDIRECT_URI}"]
                }
            }'''.format(CLIENT_ID=CLIENT_ID, CLIENT_SECRET=CLIENT_SECRET, REDIRECT_URI=REDIRECT_URI))

    app.run(debug=True)
