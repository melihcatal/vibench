import os
from flask import Flask, redirect, url_for, request, session
import google.auth.transport.requests
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "supersecretkey")

# Configuration for Google Identity Platform OIDC
CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = os.environ.get("GOOGLE_REDIRECT_URI", "http://localhost:5000/oauth2callback")

SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
]

@app.route("/oauth2callback")
def oauth2callback():
    state = session["state"]

    flow = Flow.from_client_secrets_file(
        "client_secret.json",
        scopes=SCOPES,
        state=state,
        redirect_uri=REDIRECT_URI
    )

    flow.fetch_token(authorization_response=request.url)

    credentials = flow.credentials

    # Verify the ID Token
    id_info = id_token.verify_oauth2_token(
        credentials.id_token, google.auth.transport.requests.Request(), CLIENT_ID
    )

    session["credentials"] = {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes,
        "id_token": credentials.id_token,
        "user_info": id_info
    }

    # Optionally store credentials or user info in a database

    return f"<h1>Login Successful!</h1><pre>{id_info}</pre>"

if __name__ == "__main__":
    # Ensure a dummy client_secret.json exists for demonstration
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
            }'''.format(CLIENT_ID=os.environ.get("GOOGLE_CLIENT_ID", "dummy_client_id"), CLIENT_SECRET=os.environ.get("GOOGLE_CLIENT_SECRET", "dummy_client_secret"), REDIRECT_URI=os.environ.get("GOOGLE_REDIRECT_URI", "http://localhost:5000/oauth2callback")))

    app.run(debug=True)
